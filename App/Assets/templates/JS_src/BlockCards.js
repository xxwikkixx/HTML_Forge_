



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
        
        createCard(
            BLOCK_DATA[i].Best_Predictions[0],
            parseFloat(Math.round(BLOCK_DATA[i].Best_Predictions[1] * 100000) / 1000).toFixed(2),
            BLOCK_DATA[i].Image_Crop_Path
        );
        
    }
    isValidQueue();

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
    //image = 'https://images.unsplash.com/photo-1508138221679-760a23a2285b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1267&q=80'
    // BEFORE col-md-4 col-sm-6:
    if (cardVersion = 1){
    elem = 
    '<div class="animated ' + onAppear + ' col-lg-12 mt-3 mb-3" id="' + id_Count + 'card">'
    +   '<div class="card text-white bg-dark shadow-lg">'
    +       '<img class="card-img-top" src="' + image + '" alt=" Image Not Found" style="width:100%; height: 100%; object-fit: fit;">'
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
        if(label == "!!Not Recognize!! "){ label = "Not Recognized";}
        elem = 
        '<div class="blockCard z-depth-1 hoverable row mb-2 animated delay-' + (10 + (id_Count*2)) + ' ' + onAppear + '" id="' + id_Count + 'card" onClick="cardFocus(this.id)">'
        +    '<div class="cardContent contain-content col s10">'
        +        '<div class ="cardImageOuter valign-wrapper">'
        +           '<img class="materialboxed cardImageInner" src="' + image + '">'
        +        '</div>'
        +        '<h5 id="'+ id_Count +'card_title" class="cc-tl card-title m-0">' + label + '</h5>'
        +        '<p  id="'+ id_Count +'card_prob"  class="cc-bl card-text">Probability: ' + prob + ' % </p>'
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
    BLOCK_QUEUE.push(label);
    id_Count++;
    
}

// Brings card to the top if clicked
function cardFocus(id){

    // Remove 'onTop' class from all 
    for(var i = 0; i < CURRENT_CARDS.length; i++){
        let cardID = CURRENT_CARDS[i] + 'card';
        document.getElementById(cardID).classList.remove('onTop');
    }

    // Place passed card on top
    document.getElementById(id).classList.add('onTop');
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
    CURRENT_CARDS = arrayRemove(CURRENT_CARDS, index);
    isValidQueue();

    console.log("Current Block_queue: " + BLOCK_QUEUE);
    console.log("Current Cards: "       + CURRENT_CARDS);
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
    isValidQueue();

    console.log("Current Block_queue: " + BLOCK_QUEUE);
    console.log("Current Cards: "       + CURRENT_CARDS);
}

function isValidQueue(){
    // Check for unrecognized labels in queue
    for(var i = 0; i < BLOCK_QUEUE.length; i++){
        if(BLOCK_QUEUE[i] == "Not Recognized" ) {
            $('#Generate-btn').prop('disabled', true);
            return false;
        }
    }
    // Allow user to proceed if none are found
    $('#Generate-btn').prop('disabled', false);
    return true;
}

// Deleting from an array is not native in JS, 
function arrayRemove(arr, value) {
    return arr.filter(function(ele){
        return ele != value;
    });
 }
