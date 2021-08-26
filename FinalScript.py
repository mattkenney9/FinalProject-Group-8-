def RunML(inputSmiles):

    import pandas as pd
    from chembl_webresource_client.new_client import new_client
    import random
    import string
    import collections
    import csv
    import os
    import statistics
    import numpy as np

    # Target search for coronavirus
    searchbyName = 'Acetylcholinesterase'

    target = new_client.target
    target_query = target.filter(pref_name = searchbyName).filter(target_type = 'SINGLE PROTEIN')
    targets = pd.DataFrame.from_dict(target_query)

    selected_protein = targets.target_chembl_id[1]

    def mol_query_to_list(molecule):
        return pd.DataFrame([[molecule['molecule_chembl_id'],
                            molecule['canonical_smiles'],
                            molecule['standard_value'],
                            molecule['assay_description'],
                            molecule['assay_type']]],
                            columns = ['molecule_chembl_id','canonical_smiles','standard_value','assay_description','assay_type'])



    activity = new_client.activity
    mol_query = activity.filter(target_chembl_id=selected_protein).filter(standard_type="IC50")
    #Pull select query data to list
    mol_list = list(map(mol_query_to_list, mol_query))

    df_tr = pd.DataFrame(np.concatenate(mol_list),columns = ['molecule_chembl_id','canonical_smiles','standard_value','assay_description','assay_type'])

    selection = ['molecule_chembl_id','canonical_smiles','standard_value']
    df3 = df_tr[selection]
    df3 = df3.replace(to_replace='None', value=np.nan).dropna()

    selection = ['canonical_smiles','molecule_chembl_id']
    df3_selection = df3[selection]
    df3_selection.to_csv('molecule.smi', sep='\t', index=False, header=False)

    df3['standard_value'] = pd.to_numeric(df3['standard_value'])

    os.system("java -Xms1G -Xmx1G -Djava.awt.headless=true -jar ./PaDEL-Descriptor/PaDEL-Descriptor.jar -removesalt -standardizenitro -fingerprints -descriptortypes ./PaDEL-Descriptor/PubchemFingerprinter.xml -dir ./ -file descriptors_output.csv")

    import numpy as np

    def pIC50(input):
    # import numpy as np

        pIC50 = []

        for i in input['standard_value_norm']:
            molar = i*(10**-9) # Converts nM to M
            pIC50.append(-np.log10(molar))

        input['pIC50'] = pIC50
        x = input.drop('standard_value_norm', 1)
                
        return x


    def norm_value(input):
        norm = []
        for i in input['standard_value']:
            if i > 100000000:
                i = 100000000
            norm.append(i)
        input['standard_value_norm'] = norm
        x = input.drop('standard_value', 1)
                
        return x


    

    df_norm = norm_value(df3)

    df_final = pIC50(df_norm)

    df3_X = pd.read_csv('descriptors_output.csv')
    df3_X = df3_X.drop(columns=['Name'])

    df3_Y = df_final['pIC50']
    dataset3 = pd.concat([df3_X,df3_Y], axis=1)
    finalDF = dataset3.dropna()

    X = finalDF.drop('pIC50', axis=1)
    Y = finalDF.pIC50

    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

    import numpy as np
    np.random.seed(100)
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X_train, Y_train)
    r2 = model.score(X_test, Y_test)

    Y_pred = model.predict(X_test)

    selectionSmile = inputSmiles
    selectionsmiles_df = {'canonical_smiles': [selectionSmile]
            }

    dfsearch = pd.DataFrame(selectionsmiles_df, columns = ['canonical_smiles'])

    dfsearch.to_csv('molecule.smi', sep='\t', index=False, header=False)

    os.system("java -Xms1G -Xmx1G -Djava.awt.headless=true -jar ./PaDEL-Descriptor/PaDEL-Descriptor.jar -removesalt -standardizenitro -fingerprints -descriptortypes ./PaDEL-Descriptor/PubchemFingerprinter.xml -dir ./ -file descriptors_output.csv")

    df3_X_final = pd.read_csv('descriptors_output.csv')
    df3_X_final = df3_X_final.drop(columns=['Name'])
    df3_X_final

    xInpur = df3_X_final.to_numpy()

    Y_pred = model.predict(xInpur)
    Y_pred = statistics.median(Y_pred)
    df = pd.DataFrame(data=Y_pred, index=[0], columns=["Predict"])
    import json
    # json.dumps(statistics.median(Y_pred))
    result = df.to_json()
    return result




