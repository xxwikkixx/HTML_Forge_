/*

*/ 


var id_Count = 0;
var API_UL_IMAGE = "http://localhost5000/api/imageuploaded";
var API_BLOCK_REQ = "http://localhost:5000/api/blocksdetected/"; //Add user Session Id
var API_SESSION_ID = "";
var current_Blocks;



// All Pages -> Upload Page
function resetUpload(){
    document.getElementById("upload_page").style.display = "block";     // Shows
    document.getElementById("detection_page").style.display = "none";   // Hides
    document.getElementById("results_page").style.display = "none";     // Hides
}



// Uplaod page -> Detection Page
function confirmUpload(){


    $.getJSON(API_BLOCK_REQ + API_SESSION_ID, function(data){

        user_Data = data;
        //console.log(data);

        });
    

    document.getElementById("upload_page").style.display = "none";      // Hides
    document.getElementById("detection_page").style.display = "block";  // Shows
    document.getElementById("results_page").style.display = "none";     // Hides
}



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
    // Makes a call to create and store all users
    $.getJSON(API_USER_REQ, function(data){

    current_Blocks = data;
    //console.log(data);

    makePosts();
    });
}   


// Creates building-block card 
function createCard(){

    /***** DEBUG *****/
    console.log("card" + id_Count + " Generated")

    /***** FRONT-END USE *****/
    var elem = '<div class="col-md-4 col-sm-6" id="card' + id_Count + '">'
    + '<div class="card mb-4 text-white bg-dark">'
    + '<img class="card-img-top" src="Assets/Images/ph350x350.png" alt="Card image cap">'
    + '<div class="card-body center">'
    + '<h5 class="card-title">Component</h5>'
    + '<p class="card-text">Probability: XX.XX %</p>'
    + '<ul class="list-unstyled list-inline font-small">'
    + '<li class="list-inline-item pr-2"><a class="btn btn-outline-light btn-sm right" id="card' + id_Count + '" onclick="editCard(this.id,1)">Edit Block</a></li>'
    + '<li class="list-inline-item pr-2"><a class="btn btn-outline-danger btn-sm right" id="card' + id_Count + '" onclick="deleteCard(this.id)">Delete</a></li>'
    + '</ul></div></div></div>';

    $("#detected_box").append(elem);
    //document.getElementById("detected_box").append(elem);

    //***** BACK-END USE *****/
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