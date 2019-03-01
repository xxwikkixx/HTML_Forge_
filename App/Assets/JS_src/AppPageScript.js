/*

*/ 


var id_Count = 0;

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