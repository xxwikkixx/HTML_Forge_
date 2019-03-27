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
var DEBUG_IMG;              // Stores Debugged image path returned by OpenCV with Google AI

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
    showLoading();

    // Calls an API that runs the AI function on google
    $.getJSON(API_BLOCK_CONVERT, function(data1){

        // This call retrieves the JSON returned from Google's AI
        $.getJSON(API_BLOCK_REQ + API_SESSION_ID, function(data){

            document.getElementById("loading_page").style.display = "none";      // Hides
            document.getElementById("detection_page").style.display = "block";   // Shows

            console.log(data);
            BLOCK_DATA = data.blocks;
            DEBUG_IMG = data.debugImage;
            makeCards();
        });
    });
}



/** showLoading:
 *  Shows loading page
 *      TAKES:      NONE
 *      RETURNS :   Shows Loading Page
*/
function showLoading(){
    // Show loading screen
    document.getElementById("upload_page").style.display = "none";      // Hides
    document.getElementById("loading_page").style.display = "block";    // Shows
    document.getElementById("detection_page").style.display = "none";   // Hides
    document.getElementById("results_page").style.display = "none";     // Hides
}



// FUnction similar to confirmUpload, but does not make any calls to googles real API
// Instead, it uses a prefabricated JSON: THIS IS FOR TESTING/DEBUGGING PURPOSES ONLY
function bypassUpload(){  

    document.getElementById("upload_page").style.display = "none";      // Hides
    document.getElementById("detection_page").style.display = "block";  // Shows
    document.getElementById("results_page").style.display = "none";     // Hides

    // This call retrieves a JSON SAMPLE COPY returned from Google's AI 
    //$.getJSON("https://api.myjson.com/bins/12dmxq", function(data){  // This is used for debugging
    $.getJSON("https://api.myjson.com/bins/12d9wa", function(data){
        console.log(data);
        console.log(data.blocks)
        BLOCK_DATA = data.blocks;
        makeCards();
        
    });
}


template_choice = 0;
// Detection Page -> Generation Page
function GenerateHTML(){

    // Blocks found in detection page pushed into an array in order of detection
    Populate_blocks(); 

    // Array is read and translated into appropriate HTML Code
    var code_generated = get_HTML(template_choice , block_order);

    // Prints generated HTML into div "pushed_code"
    console.log(code_generated);                                        // Debugging
    document.getElementById("pushed_code").innerText = code_generated;
    document.getElementById("upload_page").style.display = "none";      // Hides
    document.getElementById("detection_page").style.display = "none";   // Hides
    document.getElementById("results_page").style.display = "block";    // Shows
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

    var cardVersion = 2;  // 1 for new UI, 2 for new UI

    /***** DEBUG *****/
    console.log(id_Count + "card Generated")

    /***** FRONT-END USE *****/
    var elem = "";

    //image = 'http://via.placeholder.com/350x150'
    // BEFORE col-md-4 col-sm-6:
    if (cardVersion = 1){
    elem = 
    '<div class="animated ' + onAppear + ' col-lg-12 mt-3 mb-3" id="' + id_Count + 'card">'
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
    }


    if(cardVersion = 2){
        elem = 
        '<div class="blockCard z-depth-1 hoverable row col s12 mb-2 animated ' + onAppear + '" id="' + id_Count + 'card"">'
        +    '<div class="cardContent col s4">'
        +        '<h5 id="'+ id_Count +'card_title" class="card-title m-0">' + label + '</h5>'
        +        '<p  id="'+ id_Count +'card_prob"  class="card-text">Probability: ' + prob + ' % </p>'
        +    '</div>'
        +    '<div class="cardImage col s7">'
        +        '<img class="materialboxed" src="' + image + '">'
        +    '</div>'
        +    '<div class="cardButtons col s1">'
        +        '<button class="editButton waves-effect waves-light dropdown-trigger" href="#" data-target="dropdown'+ id_Count +'"><i class="material-icons">edit</i></button>'
        +        '<button class="delButton waves-effect waves-light" id="' + id_Count + 'card" onclick="deleteCard(this.id)"><i class="material-icons">delete</i></button>'
        +          '<ul id="dropdown'+ id_Count +'" class="dropdown-content">'
        +            '<li> <a id="' + id_Count + 'card" onclick="editCard(this.id, 1)">Header</a> </li>'
        +            '<li> <a id="' + id_Count + 'card" onclick="editCard(this.id, 2)">Footer</a> </li>'
        +            '<li> <a id="' + id_Count + 'card" onclick="editCard(this.id, 3)">Paragraph</a> </li>'
        +            '<li> <a id="' + id_Count + 'card" onclick="editCard(this.id, 4)">Title</a> </li>'
        +            '<li> <a id="' + id_Count + 'card" onclick="editCard(this.id, 5)">Single Image</a> </li>'
        +            '<li> <a id="' + id_Count + 'card" onclick="editCard(this.id, 6)">Slider Gallary</a> </li>'
        +            '<li> <a id="' + id_Count + 'card" onclick="editCard(this.id, 7)">Image Preview</a> </li>'
        +            '<li> <a id="' + id_Count + 'card" onclick="editCard(this.id, 8)">Gallary</a> </li>'
        +            '<li> <a id="' + id_Count + 'card" onclick="editCard(this.id, 9)" >Image-L Text-R</a> </li>'
        +            '<li> <a id="' + id_Count + 'card" onclick="editCard(this.id, 10)">Image-R Text-L</a> </li>'
        +            '<li> <a id="' + id_Count + 'card" onclick="editCard(this.id, 11)">Image-T Text-B</a>  </li>'
        +          '</ul>'
        +    '</div>'
        +'</div>';
    }
 
    // Adds new card to the box
    $("#detected_box").append(elem);
    if(cardVersion = 2) {M.AutoInit();} //For Edit Functionality when using Materialize

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
    // Copy 
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val($(element).text()).select();
    document.execCommand("copy");
    $temp.remove();

    // Alert
    alert("Succesfully copied to Clipboard");
  }


  function getZip(code) {
    // Creates a new instance
    var zip = new JSZip();

    // Create a file
    //   var html = document.getElementById("pushed_code").value();
      console.log(code);
    // zip.file("index.html", document.getElementById("pushed_code").value());
    zip.file("index.html", code);
    zip.file("layout.css", "AWH YEAH!");

    // Add images
    // zip.file("index.html", "AWH YEAH!");
    // zip.file("index.html", "AWH YEAH!");
    // zip.file("index.html", "AWH YEAH!");
 

    // create a file and a folder
    // zip.file("nested/hello.txt", "Hello World\n");

    // var img = zip.folder("images");
    // img.file("smile.gif", imgData, {base64: true});
    
    zip.generateAsync({type:"blob"})
        .then(function(content) {
            // see FileSaver.js
            saveAs(content, "example.zip");
    });
  }
  