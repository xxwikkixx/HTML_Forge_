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
var htmlFile;               // Stores an Instance of parsed HTML for live-Rendering
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
    // Adjust Scroll Bar
    $(document).scrollTop(0);
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



/** toggleDiv:
*  Toggle the display of a passed div On/Off
*/
function toggleDiv(divID) {
    var x = document.getElementById(divID);
    if (x.style.display === "none") { x.style.display = "block";} 
    else { x.style.display = "none";}
}


/** bypassUpload:
*   Function similar to confirmUpload, but does not make any calls to googles real API
*   Instead, it uses a prefabricated JSON: THIS IS FOR TESTING/DEBUGGING PURPOSES ONLY
*/
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


/** ------------------------------------------------------------------------------------- **/
/** --------------------             API CALL Handlers               -------------------- **/


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
    console.log(API_BLOCK_CONVERT + "/" + API_SESSION_ID);
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
}



/** userSelectUpload:
 *  Runs when 'Use This Image' Button is pressed and displays the detection page. 
 *  Calls an alternate route to confirmUpload
 *  Calls makeCards to generate cards based on returned JSON
 *      TAKES:      Global Variable userSelectedImage
 *      RETURNS :   NONE
*/
var userSelectedImage;  // Global Var Used for the Image
function userSelectUpload(){
    fetch(API_URL + "/upload/"+ userSelectedImage+"/Stock")
      .then(function(response) {
          return response.json();
      })
    .then(function(myJson) {
        setSessionID(JSON.stringify(myJson.id));
        console.log(API_SESSION_ID);
        API_SESSION_ID = API_SESSION_ID.replace(/['"]+/g, '');
        confirmUpload();
    });
}

// Updates Image Choice and CSS
function selectPreMade(actualID, divID){
    // Removes CSS selected Class from all
    document.getElementById("usu_1").classList.remove('selectedUpload');
    document.getElementById("usu_2").classList.remove('selectedUpload');
    document.getElementById("usu_3").classList.remove('selectedUpload');
    document.getElementById("usu_4").classList.remove('selectedUpload');
    document.getElementById("usu_5").classList.remove('selectedUpload');

    // Adds CSS to selected Element
    document.getElementById(actualID).classList.add('selectedUpload');

    // Update Selected Image
    userSelectedImage = divID;

    // Allows button to be pressed
    $('#userChoiceBtn').prop('disabled', false);     
    
    // Debugging:
    // console.log("image"+ userSelectedImage);
}

// Setter Function to update the global variable 'User Selected Image' based on user choice
function setSessionID(sId) {
    API_SESSION_ID = sId;
}



/** ------------------------------------------------------------------------------------- **/
/** --------------------           Button Click Handlers             -------------------- **/


/** GenerateHTML:
 *  Runs when 'Generate' Button is pressed. 
 *  IN:   template_choice
 *  OUT:  - Generates HTML based on template choice
 *        - Displays HTML in HTML tab
 *        - Displays CSS in CSS tab
 *        - Renders HTML in PREVIEW tab
 *        - Displays the Page Holding all these Changes
*/
function GenerateHTML(template_choice){

    // Blocks found in detection page pushed into an block_order array
    Populate_blocks(); 

    // Array is read and translated into appropriate HTML Code
    var code_generated = get_HTML(template_choice , block_order);

    // Prints generated HTML into div "pushed_code"
    console.log(code_generated);                                        // Debugging
    document.getElementById("pushed_code").innerText = code_generated;  // HTML Div
    document.getElementById("pushed_css").innerText = cssCodeString;    // CSS Div

    // Places Generated code in the preview tab
    htmlFile = new Blob([code_generated], {type: "text/html"});
    document.getElementById("PREV_space").src = URL.createObjectURL(htmlFile);

    // Reveal appropriate Pages
    tabSwitch(1);
    pageSwitch(4);
}



/** fullPrev:
 *  Displays Full-Scale Web Render of the HTML in a new tab 
 *  IN:   GLOBAL VAR: htmlFile
 *  OUT:  Opens New tab with rendered website on it
*/
function fullPrev(){
    window.open( URL.createObjectURL(htmlFile) ,'_blank')
}



/** copyToClipboard:
 *  Copies all text stored in a given div into user's clipboard. 
 *  IN:   element_id to copy from
 *  OUT:  String of all text in that div
*/
function copyToClipboard(element) {
    // Copy 
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val($(element).text()).select();
    document.execCommand("copy");
    $temp.remove();

    // Alert
    document.getElementById('copiedSuccess').style.display = "block";
}



/** getZip:
 *  Copies all text stored in HTML/CSS divs and creates zip file with them. 
 *  IN:   /
 *  OUT:  ZipFile to be downloaded
*/
function getZip() {
    // Creates a new instance
    var zip = new JSZip();

    // Get Code from the divs
    var HTMLcode = document.getElementById('pushed_code').innerText;   // HTML Div
    var CSScode  = document.getElementById("pushed_css").innerText;    // CSS Div

    // Put the files in
    zip.file("index.html", HTMLcode);
    zip.file("layout.css", CSScode);
    
    // Generate the zip file + Prompt download
    zip.generateAsync({type:"blob"})
        .then(function(content) {
            // see FileSaver.js
            saveAs(content, "YourSite.zip");
    });
}
  


/** rePos:
*   Used to adjust the position of the Upload Button on Click
*/
function rePos(divID){
  var element = document.getElementById(divID);
  element.classList.remove("upld-btn");
  element.classList.add("expand-upld-btn");
}


