/*

*/ 


var id_Count = 0;
var API_UL_IMAGE = "http://localhost5000/api/imageuploaded";
var API_BLOCK_REQ = "http://localhost:5000/api/blocksdetected/"; //Add user Session Id
var API_SESSION_ID = "hhhhhh";
var API_BLOCK_CONVERT = "http://localhost:5000/api/startconvert";

var CURRENT_CARDS = [];
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
    $.getJSON(API_BLOCK_CONVERT, function(data1){
        console.log(data1)
        $.getJSON(API_BLOCK_REQ + API_SESSION_ID, function(data){
        // $.getJSON("https://api.myjson.com/bins/12dmxq", function(data){

            //console.log("Yaaay");
            console.log(data);
            console.log(data.blocks)

            BLOCK_DATA = data.blocks;
            makeCards();
        });
    });

    document.getElementById("upload_page").style.display = "none";      // Hides
    document.getElementById("detection_page").style.display = "block";  // Shows
    document.getElementById("results_page").style.display = "none";     // Hides
}

// confirmUpload();


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
function labelAdapter(){
    block_order = [];           // Reset Blocks

    for(var i = 0; i < BLOCK_QUEUE.length; i++){
        if(BLOCK_QUEUE[i] == "Header")              {block_order.push('label_1');}  // Header
        if(BLOCK_QUEUE[i] == "Footer")              {block_order.push('label_2');}  // Footer
        if(BLOCK_QUEUE[i] == "Paragraph")           {block_order.push('label_3');}  // Paragraph
        if(BLOCK_QUEUE[i] == "Title")               {block_order.push('label_4');}  // Title
        if(BLOCK_QUEUE[i] == "singleImage")         {block_order.push('label_5');}  // Stand Alone Image
        if(BLOCK_QUEUE[i] == "Img_Gal_Parallax")    {block_order.push('label_6');}  // Slider Gallary
        if(BLOCK_QUEUE[i] == "Img_Gal_Preview")     {block_order.push('label_7');}  // Image Preview
        if(BLOCK_QUEUE[i] == "Img_Gal_Simple")      {block_order.push('label_8');}  // Image Gallary Spread
        if(BLOCK_QUEUE[i] == "Img_Left_Text_Right") {block_order.push('label_9');}  // Image-Left Text-Right 
        if(BLOCK_QUEUE[i] == "Img_Right_Text_Left") {block_order.push('label_10');} // Image-Right Text-Left
        if(BLOCK_QUEUE[i] == "Img_Top_Text_Bottom") {block_order.push('label_11');} // Image-Top Text_Bottom

    }

    console.log(block_order);
}   


// Creates all cards based on returned blocks from API
function makeCards(){

    // Empty existing Queue (MAY HAVE TO DELETE STUFF FROM HERE LATER - COULD BE A BUG FIX)
    if(CURRENT_CARDS.length > 0) {
        for(var i = 0; i < CURRENT_CARDS.length; i++){
            deleteCard(CURRENT_CARDS[i]);
        }
    }
    BLOCK_QUEUE = [];
    id_Count = 0;

    // Create a Card for the front end
    for(var i = 0; i < BLOCK_DATA.length; i++){
        createCard(
            BLOCK_DATA[i].Best_Predictions[0],
            BLOCK_DATA[i].Best_Predictions[1],
            BLOCK_DATA[i].Image_Crop_Path,
            );
        
        BLOCK_QUEUE.push(BLOCK_DATA[i].Best_Predictions[0]);
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
    CURRENT_CARDS.push(id_Count);
    id_Count++;
    
}


// Deletes a building-block card
function deleteCard(id){
    
    /***** DEBUG *****/
    console.log(id + " Deleted")
   
    /***** FRONT-END USE *****/
    var child = document.getElementById(id);
    document.getElementById("detected_box").removeChild(child);

    /***** BACK-END USE *****/
    CURRENT_CARDS.splice(CURRENT_CARDS.indexOf(id));  // Remove from array
    // ADD CODE TO REMOVE FROM BLOCK_QUEUE
}


// Edits a building-block card
function editCard(id, action){
    
    /***** DEBUG *****/
    console.log(id + " edit invoked with action " + action);
   
    /***** FRONT-END USE *****/


    /***** BACK-END USE *****/
    // Remove from array
    // ADD CODE TO EDIT FROM BLOCK_QUEUE
}