/**  BlockCards  ---------------------------------------------------------------------------
 * - This JS file is responsible for handling all card activity
 * - Dependencies: 
 *      AppPageScript.js     // Requires the global variables found in this script
 *            
 *
 * Written by: Khalid Qubbaj
 * --------------------------------------------------------------------------------------- */ 



/**  Global Variables  **/
var id_Count = 0;                   // Counter to uniquely identify Cards(Blocks)

/**  Card Animations  **/
var onAppear = 'fadeInLeft';        // Animation from Animate.css used when a card is created
var onDelete = 'zoomOut';           // Animation from Animate.css used when a card is deleted



/**       
 * Takes the label names returned from API and prettifies the label name
 * In:      API label name
 * Out:     Prettified Label name
 * **/
function prettyLabel ( plabel ) {

    if(plabel == labels[5])             {return "Single Image";}           // Stand Alone Image
    if(plabel == labels[6])             {return "Slider Gallery";}         // Slider Gallary
    if(plabel == labels[7])             {return "Image Preview";}          // Image Preview
    if(plabel == labels[8])             {return "Image Gallery";}          // Image Gallary Spread
    if(plabel == labels[9])             {return "Image-Left Text-Right";}  // Image-Left Text-Right 
    if(plabel == labels[10])            {return "Image-Right Text-Left";}  // Image-Right Text-Left
    if(plabel == labels[11])            {return "Image-Top Text-Bottom";}  // Image-Top Text-Bottom

    if(plabel == "!!Not Recognize!! ")  {return "Not Recognized";}         // Unrecognized label (AI returned)
    return plabel;              // Return Unchanged Label Otherwise
}   



/**       
 * Generates all front end cards and creates the lists passed to the AI
 * In:      Global variables (from AppPageScript):
 *              CURRENT_CARDS   -   Holds Card Ids of current cards
 *              BLOCK_QUEUE     -   Holds a list of labels (ordered); 
 *                                  used to parse the HTML.
 *              BLOCK_DATA      -   Holds all label information detected by AI   
 *              id_Count        -   Counter to uniquely assign & Identify Cards (Blocks)                                             
 * Out:     Front End - Population of Cards
 *          Back End  - Population & handling of Global variables
 * **/
function makeCards(){

    // Reset Front-End 
    document.getElementById("detected_box").innerHTML = "";

    // Reset Back-End
    CURRENT_CARDS = [];
    BLOCK_QUEUE = [];
    id_Count = 0;

    // Create the Cards for the front end based on the BLOCK_DATA's Length
        for(var i = 0; i < BLOCK_DATA.length; i++){
        
        createCard(
            BLOCK_DATA[i].Best_Predictions[0],
            parseFloat(Math.round(BLOCK_DATA[i].Best_Predictions[1] * 100000) / 1000).toFixed(2),
            BLOCK_DATA[i].Image_Crop_Path
        );
        
    }
    isValidQueue();

    /***** DEBUG *****/
    console.log("Current Block_queue: " + BLOCK_QUEUE);
    console.log("Current Cards: "       + CURRENT_CARDS);
}



/**       
 * Creates building-block card 
 * In:      label   - String for a given label
 *          prob    - Number for the probability
 *          image   - Path to the image used for the card                                             
 * Out:     Front End : Population of a single card based on params
 * **/
function createCard(label, prob, image){

    /***** FRONT-END USE *****/

    // Image overrides for UI dev
    // image = 'http://via.placeholder.com/350x150'
    // image = 'https://images.unsplash.com/photo-1508138221679-760a23a2285b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1267&q=80'
    
    // Card Generation:
    var elem = 
    '<div class="blockCard z-depth-1 hoverable row mb-2 animated delay-' + (10 + (id_Count*2)) + ' ' + onAppear + '" id="' + id_Count + 'card" onClick="cardFocus(this.id)">'
    +    '<div class="cardContent contain-content col s10">'
    +        '<div class ="cardImageOuter valign-wrapper">'
    +           '<img class="materialboxed cardImageInner" src="' + image + '">'
    +        '</div>'
    +        '<h5 id="'+ id_Count +'card_title" class="cc-tl card-title m-0">' + prettyLabel(label) + '</h5>'
    +        '<p  id="'+ id_Count +'card_prob"  class="cc-bl card-text m-0">Probability: ' + prob + ' % </p>'
    +    '</div>'
    +    '<div class="cardButtons col s2 valign-center">'
    +    '<div class="">'
    +        '<button class="editButton waves-effect waves-light dropdown-trigger" href="#" data-target="dropdown'+ id_Count +'"><i class="material-icons">edit</i></button>'
    +        '<button class="delButton waves-effect waves-light" id="' + id_Count + 'card" onclick="deleteCard(this.id)"><i class="material-icons">delete</i></button>'
    +          '<ul id="dropdown'+ id_Count +'" class="dropdown-content">'
    +            '<li> <a id="' + id_Count + 'card" onclick="editCard(this.id, 1)">Header</a> </li>'
    +            '<li> <a id="' + id_Count + 'card" onclick="editCard(this.id, 2)">Footer</a> </li>'
    +            '<li> <a id="' + id_Count + 'card" onclick="editCard(this.id, 3)">Paragraph</a> </li>'
    +            '<li> <a id="' + id_Count + 'card" onclick="editCard(this.id, 4)">Title</a> </li>'
    +            '<li> <a id="' + id_Count + 'card" onclick="editCard(this.id, 5)">Single Image</a> </li>'
    +            '<li> <a id="' + id_Count + 'card" onclick="editCard(this.id, 6)">Slider Gallery</a> </li>'
    +            '<li> <a id="' + id_Count + 'card" onclick="editCard(this.id, 7)">Image Preview</a> </li>'
    +            '<li> <a id="' + id_Count + 'card" onclick="editCard(this.id, 8)">Image Gallery</a> </li>'
    +            '<li> <a id="' + id_Count + 'card" onclick="editCard(this.id, 9)" >Image-L Text-R</a> </li>'
    +            '<li> <a id="' + id_Count + 'card" onclick="editCard(this.id, 10)">Image-R Text-L</a> </li>'
    +            '<li> <a id="' + id_Count + 'card" onclick="editCard(this.id, 11)">Image-T Text-B</a>  </li>'
    +          '</ul>'
    +    '</div>'
    +'</div>';
    
 
    // Adds new card to the box
    $("#detected_box").append(elem);
    M.AutoInit();                       // For Edit Functionality when using Materialize

    //***** BACK-END USE *****/
    CURRENT_CARDS.push(id_Count);
    BLOCK_QUEUE.push(label);
    id_Count++;

    /***** DEBUG *****/
    console.log(id_Count + "card Generated")
    
}



/**       
 * Deletes a given card from Front End Display and Back End lists
 * In:      id   - id of given card                                            
 * Out:     Label/Card Deleted
 * **/
function deleteCard(id){
   
    /***** FRONT-END USE *****/
    var child = document.getElementById(id);
    var index = parseFloat(id);

    var delayClass =  'delay-' + (10 + (index*2));
    child.classList.remove('animated', onAppear, delayClass);
    child.classList.add('animated', onDelete, 'faster');

    child.addEventListener('animationend', function() { 
        console.log(id + " Deleted")
        document.getElementById("detected_box").removeChild(child);
    })

    /***** BACK-END USE *****/
    console.log(id);
    console.log(index);
    delete BLOCK_QUEUE[index];
    CURRENT_CARDS = arrayRemove(CURRENT_CARDS, index);
    isValidQueue();

    /***** DEBUG *****/
    console.log(id_Count + "card Deleted")
    console.log("Current Block_queue: " + BLOCK_QUEUE);
    console.log("Current Cards: "       + CURRENT_CARDS);
}



/**       
 * Edits a given card by changing label name on front end and back
 * In:      id      - Id of given card    
 *          action  - The new label name the user chooses                                        
 * Out:     Edited Card
 * **/
function editCard(id, action){
    
    /***** FRONT-END USE *****/
    var title = id + '_title';
    var para = id + '_prob';
    document.getElementById(title).innerHTML =  prettyLabel(labels[action]);
    document.getElementById(para).innerHTML = "Altered by user";

    /***** BACK-END USE *****/
    var index = parseFloat(id);
    console.log(index);
    BLOCK_QUEUE[index] = labels[action];
    isValidQueue();

    /***** DEBUG *****/
    console.log(id + " edit invoked with action " + action);
    console.log("Current Block_queue: " + BLOCK_QUEUE);
    console.log("Current Cards: "       + CURRENT_CARDS);
}



/**       
 * Brings card to the top if clicked
 * In:      id   - id of given card                                            
 * Out:     Front End : gives selected card the onTop class
 * **/
function cardFocus(id){

    // Remove 'onTop' class from all 
    for(var i = 0; i < CURRENT_CARDS.length; i++){
        let cardID = CURRENT_CARDS[i] + 'card';
        document.getElementById(cardID).classList.remove('onTop');
    }

    // Place passed card on top
    document.getElementById(id).classList.add('onTop');
}



/**       
 * Checks the global variable BLOCK_QUEUE to find unlabeled cards
 * In:      Global Variable :  BLOCK_QUEUE (Holds all labels used for HTML parsing)                                     
 * Out:     Front End : Blocks/Unblocks Use of the 'Next' Button
 * **/
function isValidQueue(){
    // Check for unrecognized labels in queue
    for(var i = 0; i < BLOCK_QUEUE.length; i++){
        if(BLOCK_QUEUE[i] == "Not Recognized" ) {
            document.getElementById('detErr').style.display = "block";
            document.getElementById('detErr2').style.display = "block";
            $('#Generate-btn').prop('disabled', true);
            return false;
        }
    }
    // Allow user to proceed if none are found
    $('#Generate-btn').prop('disabled', false);
    return true;
}



// Deleting from an array is not native in JS, 
/**       
 * Deleting from an array is not native in JS; This function handles it
 * In:      Array, and value to remove                                    
 * Out:     Returns List with removed elemnent, as "" (EMPTY STRING).
 * **/
function arrayRemove(arr, value) {
    return arr.filter(function(ele){
        return ele != value;
    });
 }
