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
    
    // Show loading screen
    document.getElementById("upload_page").style.display = "none";      // Hides
    document.getElementById("loading_page").style.display = "block";    // Shows
    document.getElementById("detection_page").style.display = "none";   // Hides
    document.getElementById("results_page").style.display = "none";     // Hides

    // Calls an API that runs the AI function on google
    $.getJSON(API_BLOCK_CONVERT, function(data1){

        // This call retrieves the JSON returned from Google's AI
        $.getJSON(API_BLOCK_REQ + API_SESSION_ID, function(data){

            document.getElementById("loading_page").style.display = "none";      // Hides
            document.getElementById("detection_page").style.display = "block";   // Shows

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



/** --------------------------------  Labels & Cards  ----------------------------------- **/



var labels = [
    "",                     // index: 0   Empty
    "Header",               // index: 1   Header
    "Footer",               // index: 2   Footer
    "Paragraph",            // index: 3   Paragraph
    "Title",                // index: 4   Title
    "singleImage",          // index: 5   Stand alone image
    "Img_Gal_Parallax",     // index: 6   Slider Gallary
    "Img_Gal_Preview",      // index: 7   Image Preview
    "Img_Gal_Simple",       // index: 8   Image Gallary Spread
    "Img_Left_Text_Right",  // index: 9   Image-L Text-R
    "Img_Right_Text_Left",  // index: 10  Image-R Text-L
    "Img_Top_Text_Bottom"   // index: 11  Image-T Text-B
];


function labelAdapter(){
    block_order = [];           // Reset Blocks

    for(var i = 0; i < BLOCK_QUEUE.length; i++){
        if(BLOCK_QUEUE[i] == labels[0])     {continue;}                     // Deleted By User
        if(BLOCK_QUEUE[i] == labels[1])     {block_order.push('label_1');}  // Header
        if(BLOCK_QUEUE[i] == labels[2])     {block_order.push('label_2');}  // Footer
        if(BLOCK_QUEUE[i] == labels[3])     {block_order.push('label_3');}  // Paragraph
        if(BLOCK_QUEUE[i] == labels[4])     {block_order.push('label_4');}  // Title
        if(BLOCK_QUEUE[i] == labels[5])     {block_order.push('label_5');}  // Stand Alone Image
        if(BLOCK_QUEUE[i] == labels[6])     {block_order.push('label_6');}  // Slider Gallary
        if(BLOCK_QUEUE[i] == labels[7])     {block_order.push('label_7');}  // Image Preview
        if(BLOCK_QUEUE[i] == labels[8])     {block_order.push('label_8');}  // Image Gallary Spread
        if(BLOCK_QUEUE[i] == labels[9])     {block_order.push('label_9');}  // Image-Left Text-Right 
        if(BLOCK_QUEUE[i] == labels[10])    {block_order.push('label_10');} // Image-Right Text-Left
        if(BLOCK_QUEUE[i] == labels[11])    {block_order.push('label_11');} // Image-Top Text_Bottom

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
    //image = 'http://via.placeholder.com/350x150'
    // BEFORE col-md-4 col-sm-6:
    var elem = 
    '<div class="animated ' + onAppear + ' col-lg-6 col-xl-4 mt-3 mb-3" id="' + id_Count + 'card">'
    +   '<div class="card text-white bg-dark shadow-lg">'
    +       '<img class="card-img-top" src="' + image + '" alt=" Image Not Found" style="width: 100%; height: 150px; object-fit: fill;">'
    +       '<div class="card-body center">'
    +           '<h5 id="'+ id_Count +'card_title" class="card-title m-0">' + label + '</h5>'
    +           '<p  id="'+ id_Count +'card_prob" class="card-text">Probability: ' + prob + ' % </p>'
    +                   '<div class="btn-group dropup">'
    +                       '<button type="button" class="btn btn-sm btn-danger dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"> Edit Block </button>'
    +                       '<div class="dropdown-menu">'
    +                           '<a class="dropdown-item" id="' + id_Count + 'card" onclick="editCard(this.id, 1)">Header</a>'
    +                           '<a class="dropdown-item" id="' + id_Count + 'card" onclick="editCard(this.id, 2)">Footer</a>'
    +                           '<a class="dropdown-item" id="' + id_Count + 'card" onclick="editCard(this.id, 3)">Paragraph</a>'
    +                           '<a class="dropdown-item" id="' + id_Count + 'card" onclick="editCard(this.id, 4)">Title</a>'
    +                           '<a class="dropdown-item" id="' + id_Count + 'card" onclick="editCard(this.id, 5)">Single Image</a>'
    +                           '<a class="dropdown-item" id="' + id_Count + 'card" onclick="editCard(this.id, 6)">Slider Gallary</a>'
    +                           '<a class="dropdown-item" id="' + id_Count + 'card" onclick="editCard(this.id, 7)">Image Preview</a>'
    +                           '<a class="dropdown-item" id="' + id_Count + 'card" onclick="editCard(this.id, 8)">Gallary</a>'
    +                           '<a class="dropdown-item" id="' + id_Count + 'card" onclick="editCard(this.id, 9)" >Image-L Text-R</a>'
    +                           '<a class="dropdown-item" id="' + id_Count + 'card" onclick="editCard(this.id, 10)">Image-R Text-L</a>'
    +                           '<a class="dropdown-item" id="' + id_Count + 'card" onclick="editCard(this.id, 11)">Image-T Text-B</a>'           
    +                       '</div>'
    +                   '</div>'
    +                   '<button class="btn btn-sm btn-outline-danger right" id="' + id_Count + 'card" onclick="deleteCard(this.id)">Delete</button>'
    + '</div></div></div>';



    // Alternate style
    // var elem = 
    //     '<div class= "col-lg-6 col-xl-4 mt-3">'
    // +       '<div class="card text-center animated bg-dark text-white">'
    // +           '<div class="card-header">' + label + '</div>'
    // +           '<div class="card-body">'
    // +               '<img class="card-img-mid" src="' + image + '" alt=" Image Not Found" style="width: 100%; height: 15vw; object-fit: cover;">'
    // +           '</div>'
    // +           '<div class="card-footer text-muted">Probability: ' + prob + ' %</div>'
    // +       '</div>'
    // +    '</div>';
 

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
    var title = id + '_title';
    var para = id + '_prob';
    document.getElementById(title).innerHTML = labels[action];
    document.getElementById(para).innerHTML = "Altered by user";

    /***** BACK-END USE *****/
    var index = parseFloat(id);
    console.log(index);
    BLOCK_QUEUE[index] = labels[action];

    console.log("Current Block_queue: " + BLOCK_QUEUE);
    console.log("Current Cards: "       + CURRENT_CARDS);
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
  