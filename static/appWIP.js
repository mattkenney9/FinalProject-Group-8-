function init() {
    //Load Data
  
    /* data route */
    const SmilesDataurl = "/api/getSmilesData";
  
    d3.csv(SmilesDataurl).then(function (response) {
      // console.log(response);
  
      var importedData = response;
  
      // debugger;
      var smile =importedData[0].Smiles
    //   d3.select("#inputsmiles").property("value") == smile
      document.getElementById("outputsmiles").value = smile;
     
  
    });
  }
  
  function storeMessage() {
    var smileInput = d3.select("#inputsmiles").property("value");
    // debugger;
    const storeSmilesDataurl = "/api/storeSmilesData";
    $.ajax({
        type:"GET",
        dataType: "json",
        data:{'name':smileInput},
        url: storeSmilesDataurl,
        success: function(data){
            buf1=data;
            console.log(data);
            init();
        }
    })
    
    // debugger;


    const RunMLURL = "/api/RunML";
    $.ajax({
        type:"GET",
        dataType: "json",
        data:{'name':smileInput},
        url: RunMLURL,
        success: function(data){
            buf2=data;
            console.log(data);
            LoadMLOutput(data);
        }
    })


  }
  

  function LoadMLOutput(output){
    debugger;
    var outputvalue = output.Predict[0]
    // const obj = JSON.parse(output)
    document.getElementById("outputsmiles").value = outputvalue;
  }

  // Initializes the page with a default
  init();
  
  