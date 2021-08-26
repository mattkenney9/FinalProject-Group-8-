// Select the button
var button = d3.select("#chembl_button");

// Select the form
var form = d3.select("#c_form");
var chemblBox = d3.select("#chembl-box");

// Create event handlers 
button.on("click", runEnter);
form.on("submit",runEnter);

// Complete the event handler function for the form
function runEnter() {
   
   // Prevent the page from refreshing
  d3.event.preventDefault();
  
  // Select the input element and get the raw HTML node
  var inputElement = d3.select("#chembl-form-input");

  // Get the value property of the input element
  var inputValue = inputElement.property("value");
  var url="https://www.ebi.ac.uk/chembl/embed/#compound_report_card/"+inputValue+"0/name_and_classification";


  console.log(inputValue);
  console.log(url);

  // Then, select the embedded chembl data
  var chemblData = d3.select("#url_id");
  //var chemblData = d3.select("object:nth-child(9)");
  
  console.log(chemblData);

  // clear link in <object> tag
  // chemblData.html("");
  chemblBox.html(`<object id="url_id" data=${url} width="100%" height="400px"></object>`) 
  
  // change the link in the <object> tag
  // chemblData.attr("data",url);

};

// $("form#c_form").on("submit",event=>{
//   console.log("****")
//   event.preventDefault()
//   $.ajax({
//     url: "https://www.ebi.ac.uk/chembl/embed/#compound_report_card/"+$("#chembl-form-input").val()+"0/name_and_classification",
//     method:"get",
//     success: result=>console.log(result), 
//     error: error=>console.log(error)
//   })
// })

//<object id="url_id"  width="100%" height="400px"></object>