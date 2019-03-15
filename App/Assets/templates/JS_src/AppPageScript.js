/** AppPageScript ---------------------------------------------------------------------------
 * - This JS file is responsible for handling all JS activity taking place on the AppPage
 * - Dependencies: 
 *      HTML_Parser_JS.js       // Handles HTML Parsing of all blocks detected
 *      Upload.js               // Handles API activity and Animation behaviour       
 *
 * Written by: Khalid Qubbaj
 * --------------------------------------------------------------------------------------- */ 



/** ------------------------------------- API CALLS ------------------------------------- **/
var API_UL_IMAGE = "http://localhost5000/api/imageuploaded";        // API to retrieve Image
var API_BLOCK_CONVERT = "http://localhost:5000/api/startconvert";   // API that calls the AI
var API_BLOCK_REQ = "http://localhost:5000/api/blocksdetected/";    // MUST ADD Session Id
var API_SESSION_ID = "ERROR";          // This gets populated by the API call from Upload.js
/** ------------------------------------------------------------------------------------- **/



/** --------------------------------- GLOBAL VARIABLES ---------------------------------- **/
var id_Count = 0;           // Counter to uniquely identify Cards(Blocks)
var CURRENT_CARDS = [];     // Keeps track of all cards currently visible on the page
var BLOCK_QUEUE = [];       // A Queue which is populated with labels, in order of which they
                            // Are found
var BLOCK_DATA;             // Stores JSON data returned by the Google AI


/** Card Animations **/
var onAppear = 'fadeIn';    // Animation from Animate.css used when a card is created
var onDelete = 'fadeOut';   // Animation from Animate.css used when a card is deleted
/** ------------------------------------------------------------------------------------- **/



/** ResetUpload:
 *  Re-displays the Upload Div from any button that calls it, will hide other pages
 *      TAKES:      NONE
 *      RETURNS :   NONE
*/
function resetUpload(){
    // Pages
    document.getElementById("upload_page").style.display = "block";     // Shows
    document.getElementById("detection_page").style.display = "none";   // Hides
    document.getElementById("results_page").style.display = "none";     // Hides
    // Components
    $('#confirm_button').prop('disabled', true);  // Blocks button from being pressed
}



/** confirmUpload:
 *  Runs when 'Convert' Button is pressed and displays the detection page. 
 *  Calls API to run AI based on uploaded Image
 *  Calls API to return JSON 
 *  Calls makeCards to generate cards based on returned JSON
 *      TAKES:      NONE
 *      RETURNS :   NONE
*/
function confirmUpload(){
    
    // Calls an API that runs the AI function on google
    $.getJSON(API_BLOCK_CONVERT, function(data1){

        document.getElementById("upload_page").style.display = "none";      // Hides
        document.getElementById("detection_page").style.display = "block";  // Shows
        document.getElementById("results_page").style.display = "none";     // Hides

        // This call retrieves the JSON returned from Google's AI
        $.getJSON(API_BLOCK_REQ + API_SESSION_ID, function(data){
            BLOCK_DATA = data.blocks;
            makeCards();
        });
    });
}


// FUnction similar to confirmUpload, but does not make any calls to googles real API
// Instead, it uses a prefabricated JSON: THIS IS FOR TESTING/DEBUGGING PURPOSES ONLY
function bypassUpload(){  

    document.getElementById("upload_page").style.display = "none";      // Hides
    document.getElementById("detection_page").style.display = "block";  // Shows
    document.getElementById("results_page").style.display = "none";     // Hides

    // This call retrieves a JSON SAMPLE COPY returned from Google's AI 
    $.getJSON("https://api.myjson.com/bins/12dmxq", function(data){  // This is used for debugging

        console.log(data);
        console.log(data.blocks)
        BLOCK_DATA = data.blocks;
        makeCards();
        
    });
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



/***********************          ************************/
function labelAdapter(){
    block_order = [];           // Reset Blocks

    for(var i = 0; i < BLOCK_QUEUE.length; i++){
        if(BLOCK_QUEUE[i] == "")                    {continue;}                     // Deleted By User
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

    // Reset Front-End 
    document.getElementById("detected_box").innerHTML = "";

    // Reset Back-End
    CURRENT_CARDS = [];
    BLOCK_QUEUE = [];
    id_Count = 0;

    // Create a Card for the front end
    for(var i = 0; i < BLOCK_DATA.length; i++){
        
      //  setTimeout(
            createCard(
                BLOCK_DATA[i].Best_Predictions[0],
                parseFloat(Math.round(BLOCK_DATA[i].Best_Predictions[1] * 100000) / 1000).toFixed(2),
                BLOCK_DATA[i].Image_Crop_Path);
       // ,1000);
        
        BLOCK_QUEUE.push(BLOCK_DATA[i].Best_Predictions[0]);
    }

    console.log("Current Block_queue: " + BLOCK_QUEUE);
    console.log("Current Cards: "       + CURRENT_CARDS);
}


// Creates building-block card 
function createCard(label, prob, image){

    /***** DEBUG *****/
    console.log(id_Count + "card Generated")

    /***** FRONT-END USE *****/
    // BEFORE col-md-4 col-sm-6:
    var elem = '<div class="animated ' + onAppear + ' col-md-6 col-lg-4" id="' + id_Count + 'card">'
    + '<div class="card mb-4 text-white bg-dark">'
    + '<img class="card-img-top" src="' + image + '" alt=" Image Not Found">'
    + '<div class="card-body center">'
    + '<h5 class="card-title">' + label + '</h5>'
    + '<p class="card-text">Probability: ' + prob + ' % </p>'
    + '<ul class="list-unstyled list-inline font-small">'
    + '<li class="list-inline-item pr-2"><a class="btn btn-outline-light btn-sm right" id="' + id_Count + 'card" onclick="editCard(this.id,1)">Edit Block</a></li>'
    + '<li class="list-inline-item pr-2"><a class="btn btn-outline-danger btn-sm right" id="' + id_Count + 'card" onclick="deleteCard(this.id)">Delete</a></li>'
    + '</ul></div></div></div>';

    $("#detected_box").append(elem);

    //***** BACK-END USE *****/
    CURRENT_CARDS.push(id_Count);
    id_Count++;
    
}


// Deletes a building-block card
function deleteCard(id){
    
    /***** DEBUG *****/
   
   
    /***** FRONT-END USE *****/
    var child = document.getElementById(id);

    child.classList.remove('animated', onAppear);
    child.classList.add('animated', onDelete, 'faster');

    child.addEventListener('animationend', function() { 
        console.log(id + " Deleted")
        document.getElementById("detected_box").removeChild(child);
    })

    /***** BACK-END USE *****/
    var index = parseFloat(id);
    console.log(id);
    console.log(index);
    delete BLOCK_QUEUE[index];
    //BLOCK_QUEUE = arrayRemove(BLOCK_QUEUE, '')
    CURRENT_CARDS = arrayRemove(CURRENT_CARDS, index)

    console.log("Current Block_queue: " + BLOCK_QUEUE);
    console.log("Current Cards: "       + CURRENT_CARDS);
}


// Deleting from an array is not native in JS, 
// 
function arrayRemove(arr, value) {
    return arr.filter(function(ele){
        return ele != value;
    });
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



// Function that handles copying to clipboard (GENERIC)
function copyToClipboard(element) {
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val($(element).text()).select();
    document.execCommand("copy");
    $temp.remove();
    alert("Succesfully copied to Clipboard");
  }
  