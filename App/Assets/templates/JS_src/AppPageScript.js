/** AppPageScript ---------------------------------------------------------------------------
 * - This JS file is responsible for handling all JS activity taking place on the AppPage
 * - Dependencies: 
 *      HTML_Parser_JS.js       // Handles HTML Parsing of all blocks detected
 *      Upload.js               // Handles API activity and Animation behaviour       
 *
 * Written by: Khalid Qubbaj
 * --------------------------------------------------------------------------------------- */ 







/** --------------------------------- GLOBAL VARIABLES ---------------------------------- **/
var CURRENT_CARDS = [];     // Keeps track of all cards currently visible on the page
var BLOCK_QUEUE = [];       // A Queue which is populated with labels, in order of which they
                            // Are found
var BLOCK_DATA;             // Stores JSON data returned by the Google AI
var DEBUG_IMG;              // Stores Debugged image path returned by OpenCV with Google AI
/** ------------------------------------------------------------------------------------- **/



/** ------------------------------------------------------------------------------------- **/
/** --------------------            Page & Tab Handlers              -------------------- **/


/** tabSwitch:
 *  Displays the requested tab and hides all others
 *      TAKES:      Tab number
 *      RETURNS :   NONE
*/
function tabSwitch(tab) {
    // Hides All
    document.getElementById("HTML_space").style.display = "none";
    document.getElementById("CSS_space").style.display  = "none";   
    document.getElementById("PREV_space").style.display = "none";
    document.getElementById("tab_HTML").classList.remove('tab-btn-selected');
    document.getElementById("tab_CSS").classList.remove('tab-btn-selected');
    document.getElementById("tab_PREV").classList.remove('tab-btn-selected');

    // Switch to requested tab
    if(tab == 1) {  document.getElementById("HTML_space").style.display = "block";
                    document.getElementById("tab_HTML").classList.add('tab-btn-selected');}  
    if(tab == 2) {  document.getElementById("CSS_space").style.display  = "block";
                    document.getElementById("tab_CSS").classList.add('tab-btn-selected');}  
    if(tab == 3) {  document.getElementById("PREV_space").style.display = "block";
                    document.getElementById("tab_PREV").classList.add('tab-btn-selected');}  
  }


/** pageSwitch:
 *  Displays the requested page and hides all others
 *      TAKES:      Tab number
 *      RETURNS :   NONE
*/
function pageSwitch(page) {
    // Hides All
    document.getElementById("upload_page").style.display    = "none";
    document.getElementById("loading_page").style.display   = "none";
    document.getElementById("detection_page").style.display = "none";
    document.getElementById("results_page").style.display   = "none";
    // Switch to requested page
    if(page == 1) {document.getElementById("upload_page").style.display    = "block"; progSwitch(1)}  
    if(page == 2) {document.getElementById("loading_page").style.display   = "block"; }  
    if(page == 3) {document.getElementById("detection_page").style.display = "block"; progSwitch(2)}  
    if(page == 4) {document.getElementById("results_page").style.display   = "block"; progSwitch(3)}  
  }


/** progSwitch:
 *  Displays the current progress and hides all others
 *      TAKES:      Tab number
 *      RETURNS :   NONE
*/
function progSwitch(prog) {

    // For animation
    var prog_id;
    if(prog == 2){ prog_id = "pb1";}    // Get previous image
    if(prog == 3){ prog_id = "pb2";}    // Get previous image
    
    // Animate the previous Image
    var child = document.getElementById(prog_id);
    child.classList.remove('animated', 'fadeIn')
    child.classList.add('animated', 'fadeOut');

    // Wait until animation is completed
    child.addEventListener('animationend', function() { 
        
        // Hides All
        document.getElementById("pb1").style.display = "none";
        document.getElementById("pb2").style.display = "none";
        document.getElementById("pb3").style.display = "none";

        // Switch to requested progress
        if(prog == 1) {document.getElementById("pb1").style.display = "block";}  
        if(prog == 2) {document.getElementById("pb2").style.display = "block";}  
        if(prog == 3) {document.getElementById("pb3").style.display = "block";}  

    })
 
  }


  /** Toggle show of a div
   * 
   */
  function toggleDiv(divID) {
    var x = document.getElementById(divID);
    if (x.style.display === "none") { x.style.display = "block";} 
    else { x.style.display = "none";}
  }


// $.ajax({
//     url: API_URL ,
//                 crossDomain: true,
//                 headers: {
//                       "accept": "application/json",
//                       "Access-Control-Allow-Origin":"*"
//                   },
//                 success: function (data) {
//                     console.log("OK")
//                 },
//                 error: function (xhr, status) {
//                     alert("error");
//                 }
//             });


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
    pageSwitch(2);

    $.ajax({
        url: API_BLOCK_CONVERT + "/" + API_SESSION_ID,
        dataType: "json",
        crossDomain: true,
        headers: {
              "accept": "application/json",
              "Access-Control-Allow-Origin":"*"
          },
        success: function (data1) {
            $.ajax({
                url: API_BLOCK_REQ + API_SESSION_ID,
                dataType: "json",
                crossDomain: true,
                headers: {
                      "accept": "application/json",
                      "Access-Control-Allow-Origin":"*"
                  },
                success: function (data) {
                    pageSwitch(3);

                    console.log(data);
                    BLOCK_DATA = data.blocks;
                    DEBUG_IMG = data.debugImage;
                    //DEBUG_IMG = "Images/Samples/Samp1.jpg"
                    document.getElementById("uploaded_img").src = DEBUG_IMG;
                    makeCards();
                },
                error: function (xhr, status) {
                    alert("error");
                }
            });

        },
        error: function (xhr, status) {
            alert("error");
        }
    });

    // Calls an API that runs the AI function on google
    // $.getJSON(API_BLOCK_CONVERT, function(data1){
    //
    //     // This call retrieves the JSON returned from Google's AI
    //     $.getJSON(API_BLOCK_REQ + API_SESSION_ID, function(data){
    //
    //         document.getElementById("loading_page").style.display = "none";      // Hides
    //         document.getElementById("detection_page").style.display = "block";   // Shows
    //
    //         console.log(data);
    //         BLOCK_DATA = data.blocks;
    //         DEBUG_IMG = data.debugImage;
    //         makeCards();
    //     });
    // });
}


function rePos(divID){
    var element = document.getElementById(divID);
    element.classList.remove("upld-btn");
    element.classList.add("expand-upld-btn");
}

// Function similar to confirmUpload, but does not make any calls to googles real API
// Instead, it uses a prefabricated JSON: THIS IS FOR TESTING/DEBUGGING PURPOSES ONLY
function bypassUpload(){  

    pageSwitch(3); //Detection Page

    // This call retrieves a JSON SAMPLE COPY returned from Google's AI 
    //$.getJSON("https://api.myjson.com/bins/12dmxq", function(data){  // This is used for debugging
    $.getJSON("https://api.myjson.com/bins/12d9wa", function(data){
        console.log(data);
        console.log(data.blocks)
        BLOCK_DATA = data.blocks;
        makeCards();
        
    });
}




var htmlFile;
// Detection Page -> Generation Page
function GenerateHTML(template_choice){

    // Blocks found in detection page pushed into an array in order of detection
    Populate_blocks(); 

    // Array is read and translated into appropriate HTML Code
    var code_generated = get_HTML(template_choice , block_order);

    // Prints generated HTML into div "pushed_code"
    console.log(code_generated);                                        // Debugging
    document.getElementById("pushed_code").innerText = code_generated;

    // Places Generated code in the preview tab
    htmlFile = new Blob([code_generated], {type: "text/html"});
    document.getElementById("PREV_space").src = URL.createObjectURL(htmlFile);

    // Reveal appropriate Pages
    tabSwitch(1);
    pageSwitch(4);
}

function fullPrev(){
    window.open( URL.createObjectURL(htmlFile) ,'_blank')
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
    zip.file("layout.css", cssCodeString);

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
  
 
  $("#btn-save").click( function() {
    var text = document.getElementById("pushed_code").innerText
    var filename = $("#index").val()
    var htmlFile = new Blob([text], {type: "text/html"});
    document.getElementById("PREV_space").src = URL.createObjectURL(htmlFile);
  });

$("#tab_CSS").click(function () {
//     console.log("Css");
//     var reader = new FileReader();
//     reader.onload = function(e) {
//         var text = reader.result;
//         console.log(text)
//     };
//     var file = File('Generated/template-1/layout.css');
//     reader.readAsText(file);

    // fetch('http://htmlforge.com/Generated/template-1/layout.css')
    //     { mode: 'no-cors'})
        // .then(function(response) {
        //     console.log(response); // "opaque"
        // });
    document.getElementById("pushed_css").innerText = cssCodeString;
    console.log(cssCodeString);
});



  $("#btn-css").click( function() {
      console.log("Css");
    fetch('/Generated/template-1/layout.css')
    .then(response => response.text())
    .then(text => console.log(text))
    // outputs the content of the text file

    // var text = document.getElementById("pushed_code").innerText
    // var filename = $("#index").val()
    // var htmlFile = new Blob([text], {type: "text/html"});
    // document.getElementById("PREV_space").src = URL.createObjectURL(htmlFile);
  });




/**------------------------------ FUNCTIONS TO BE DELETED --------------------------------------*/


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