/*

*/ 


var id_Count = 0;
var API_UL_IMAGE = "http://localhost5000/api/imageuploaded";
var API_BLOCK_REQ = "http://localhost:5000/api/blocksdetected/"; //Add user Session Id
var API_SESSION_ID = "hhhhhh";

var BLOCK_QUEUE = [];
var BLOCK_DATA;


function test(){
    console.log(API_BLOCK_REQ+API_SESSION_ID);
}

// All Pages -> Upload Page
function resetUpload(){
    document.getElementById("upload_page").style.display = "block";     // Shows
    document.getElementById("detection_page").style.display = "none";   // Hides
    document.getElementById("results_page").style.display = "none";     // Hides
    document.getElementById("confirm_button" ).style.display = "none";     // Hides
}

// Uplaod page -> Detection Page
function confirmUpload(){

    // Calls the 
    $.getJSON(API_BLOCK_REQ + API_SESSION_ID, function(data){
    // $.getJSON("https://api.myjson.com/bins/12dmxq", function(data){

        console.log("Yaaay");
        console.log(data);
        console.log(data.blocks)
       
        BLOCK_DATA = data.blocks;
        makeCards();
    });

    document.getElementById("upload_page").style.display = "none";      // Hides
    document.getElementById("detection_page").style.display = "block";  // Shows
    document.getElementById("results_page").style.display = "none";     // Hides
}

//confirmUpload();



// Detection Page -> Generation Page
function GenerateHTML(){

    // Blocks found in detection page pushed into an array in order of detection
    Populate_blocks(); 
    // Array is read and translated into appropriate HTML Code
    var code_generated = make_HTML_Basic(block_order);

    // Prints generated HTML into div "pushed_code"
    console.log(code_generated);                                        // Debugging
    document.getElementById("pushed_code").innerText = code_generated;

    document.getElementById("upload_page").style.display = "none";      // Hides
    document.getElementById("detection_page").style.display = "none";   // Hides
    document.getElementById("results_page").style.display = "block";    // Shows
}


// Create 
function convertBlocks(){}



/***********************     Creates users using API     ************************/
function readBlocks(){
    block_order = [];           // Reset Blocks

    // for(var i = 0; i < BLOCK_DATA.length; i++){
    //     var
    //     block_order.push(data[i].ID);
    // }

    // // console.log(data.blocks.length)
    // console.log(data.blocks[0])                        // All block data
    // console.log(data.blocks[0].Best_Predictions[0])    // Label
    // console.log(data.blocks[0].Best_Predictions[0])    // Prediction %



    // block_order.push('label_1');
    // block_order.push('label_3');    // Paragraph
    // block_order.push('label_4');    // Title
    // block_order.push('label_5');    // One image
    // block_order.push('label_6');    // Image Banner (Slider)
    // block_order.push('label_7');    // Image Preview
    // block_order.push('label_8');    // Image Gallary
    // block_order.push('label_9');    // Text Right Image Left
    // block_order.push('label_10');   // Text Left Image RIght
    // block_order.push('label_11');   // Text Bot Image Top
    // block_order.push('label_2');

    console.log(block_order);

}   


// Creates all cards based on returned blocks from API
function makeCards(){

    // Empty existing Queue (MAY HAVE TO DELETE STUFF FROM HERE LATER - COULD BE A BUG FIX)
    BLOCK_QUEUE = [];

    // Create a Card for the front end
    for(var i = 0; i < BLOCK_DATA.length; i++){
        createCard(
            BLOCK_DATA[i].Best_Predictions[0],
            BLOCK_DATA[i].Best_Predictions[1],
            BLOCK_DATA[i].Image_Crop_Path,
            );
    }

}


// Creates building-block card 
function createCard(label, prob, image){

    /***** DEBUG *****/
    console.log("card" + id_Count + " Generated")

    /***** FRONT-END USE *****/
    var elem = '<div class="col-md-4 col-sm-6" id="card' + id_Count + '">'
    + '<div class="card mb-4 text-white bg-dark">'
    + '<img class="card-img-top" src="' + image + '" alt="Card image cap">'
    + '<div class="card-body center">'
    + '<h5 class="card-title">' + label + '</h5>'
    + '<p class="card-text">' + prob + '% </p>'
    + '<ul class="list-unstyled list-inline font-small">'
    + '<li class="list-inline-item pr-2"><a class="btn btn-outline-light btn-sm right" id="card' + id_Count + '" onclick="editCard(this.id,1)">Edit Block</a></li>'
    + '<li class="list-inline-item pr-2"><a class="btn btn-outline-danger btn-sm right" id="card' + id_Count + '" onclick="deleteCard(this.id)">Delete</a></li>'
    + '</ul></div></div></div>';

    $("#detected_box").append(elem);

    //***** BACK-END USE *****/
    //BLOCK_QUEUE.push()
    id_Count++;


    // Add into array
}


// Deletes a builidng-block card
function deleteCard(id){
    
    /***** DEBUG *****/
    console.log(id + " Deleted")
   
    /***** FRONT-END USE *****/
    var child = document.getElementById(id);
    document.getElementById("detected_box").removeChild(child);

    /***** BACK-END USE *****/
    // Remove from array
}


// Deletes a builidng-block card
function editCard(id, action){
    
    /***** DEBUG *****/
    console.log(id + " edit invoked with action " + action);
   
    /***** FRONT-END USE *****/


    /***** BACK-END USE *****/
    // Remove from array
}