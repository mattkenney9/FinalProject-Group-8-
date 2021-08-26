# %%
import datetime as dt
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, flash
#from flask import Flask
from sqlalchemy import create_engine, MetaData
from sqlalchemy import sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import sqlite3
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
import sqlite3
import json
import FinalScript

from sqlalchemy.sql.expression import false

# %%
# Variable to hold csv files
csvfile = ["Resources/Smiles.csv"]

# Setup database
engine = create_engine("sqlite:///SmilesData.sqlite")
conn = engine.connect()


# %%
# Refelct existing database into new one
Base = declarative_base()


# %%


# %%
Base.metadata.create_all(engine)
metadata = MetaData(bind=engine)
metadata.reflect()


# %%
###
# Use Pandas to read csv into a list of row objects
###

SmilesData = pd.read_csv(csvfile[0], dtype=object)
Smiles = SmilesData.to_dict(orient='records')
Smiles = pd.DataFrame(Smiles)
# help(Smiles)
# %%
SmilesData = Smiles.to_sql('SmilesData', con=engine, if_exists='replace')

engine.execute("SELECT * FROM SmilesData").fetchall()


# %%
# Create our session (link) from Python to the DB
session = Session(engine)

# Collect the names of tables within the database
# inspector = inspect(engine)
# inspector.get_table_names()

# run ML data


# %%
# Flask setup and routes

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index')
def index1():
    return render_template('index.html')



@app.route("/api/getSmilesData")
def getsmilesdata():

    con = sqlite3.connect("SmilesData.sqlite")
    df = pd.read_sql_query(
        "select Smiles from SmilesData", con)

    return df.to_csv()

@app.route("/api/storeSmilesData",methods=['GET','POST'])
def hello_world(name=None):
    buf1 = request.args.get('name')
    str = {'key':'Hello World!', 'q':buf1}
    conn = None
    conn = sqlite3.connect("SmilesData.sqlite")
    cursor = conn.cursor()
    sql = '''UPDATE SmilesData SET Smiles=\'''' +buf1 + '''' '''
    cursor.execute(sql)
    conn.commit()
    conn = None
    
    res = json.dumps(str)
    return res

@app.route("/api/RunML",methods=['GET','POST'])
def RunML(name=None):
    buf2 = request.args.get('name')
    str = {'key':'Hello World!', 'q':buf2}
   
    output = FinalScript.RunML(buf2)
    # strr = {output
    # res = json.dumps(str)
    return output

if __name__ == '__main__':
    app.run(debug=True)


# %%
