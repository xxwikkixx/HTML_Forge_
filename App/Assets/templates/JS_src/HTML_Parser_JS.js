/*

*/ 



/** Holds Order of detected blocks **/
var block_order= [];



/** Holds images used to randomly populate image placeholders on the site **/
var stock_images = [];



/**  Holds random Lorem Ipsum statements for random text generation**/
var rand_lorem_para = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    "Integer auctor sapien ac varius gravida. Vivamus justo elit, luctus id sollicitudin et, semper ut mauris.",
    "Etiam tincidunt aliquet risus, ac euismod massa faucibus vel.", "Quisque vel tincidunt lacus.", 
    "Aliquam sit amet ante arcu.", "Vestibulum facilisis fermentum leo in laoreet.", "Nunc nec est diam.", 
    "Pellentesque facilisis justo eu diam consequat suscipit.", "Duis eu ipsum et purus condimentum convallis.",
    "Fusce magna urna, rhoncus et odio vel, porttitor consectetur sapien.", "Fusce at auctor lorem.",
    "Maecenas sit amet ultrices dui, quis mollis tellus.","Vestibulum tempor at purus eget pulvinar.",
    "Vestibulum pellentesque sem orci, non tincidunt dolor tincidunt quis.", "Etiam nec faucibus neque.",
    "Maecenas eget lorem dignissim, ultrices leo pellentesque, vehicula tortor.",
    "Nunc fringilla, eros nec imperdiet eleifend, sapien ligula mollis leo, eleifend viverra est purus ac neque.",
    "Etiam iaculis a mi quis efficitur.", "Donec dignissim varius quam id imperdiet.",
    "Nulla tincidunt erat vel arcu vulputate, eget rutrum neque sodales.", "Maecenas vel bibendum nunc.",
    "Nunc ut dui viverra, feugiat enim quis, condimentum odio.", "Ut tincidunt quis neque eu porttitor.",
    "Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.",
    "Suspendisse vel gravida arcu, eget mattis neque.", "Curabitur tristique congue tempus. Sed vel purus augue.",
    "Duis placerat metus ex, ut porta dolor pharetra non.", "Integer facilisis hendrerit quam sit amet commodo.",
    "Aliquam libero lectus, accumsan in pharetra in, ullamcorper in libero.",
    "Sed ac elit congue, efficitur lorem ac, pretium nibh.","Morbi viverra eros sed augue porttitor mollis.",
    "Donec dapibus pretium elit, in elementum ante bibendum ut.", "Cras scelerisque a ex egestas ornare.",
    "Duis euismod tincidunt nibh, in maximus magna venenatis sit amet.", "Fusce laoreet pellentesque lectus in blandit.", 
    "Morbi efficitur blandit metus, eu convallis nunc venenatis eu.", "Ut nisl dui, posuere at ligula id, eleifend hendrerit ex.",
    "Mauris lobortis, eros vel lobortis suscipit, turpis justo dictum nunc, sit amet tristique ex massa non purus.",
    "In et bibendum purus. Nulla facilisi. Maecenas mattis pellentesque congue.", "Sed a lectus et leo commodo dictum.",
    "Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae;", 
    "Sed posuere ante at ipsum porttitor, vel ultricies leo tempor.","Ut dictum ut orci quis pellentesque.", 
    "Praesent elit tellus, interdum eget ornare commodo, rhoncus quis nibh.", "Maecenas laoreet sit amet dui a cursus.",
    "Donec sed convallis sapien, ut pharetra enim.", "Fusce faucibus metus sed dui posuere suscipit.",
    "Pellentesque convallis posuere odio, at sollicitudin mauris blandit eget.", "Mauris et rutrum felis.",
    "Ut erat tellus, malesuada sit amet sagittis non, consequat vitae nisl.",
    "Praesent enim arcu, volutpat id elit eu, hendrerit aliquam odio.",
    "Aenean posuere nibh erat, vel condimentum turpis condimentum quis.",
    "Vivamus vehicula sem sit amet odio iaculis, tempor suscipit dolor porta.",
];



/**  Holds random Lorem Ipsum Titles for random title generation**/
var rand_lorem_title = [
    "Lorem ipsum dolor",  
    "Aliquam sit amet ante arcu.", 
    "Quisque vel tincidunt lacus.", 
    "Fusce at auctor lorem.",
    "Nunc nec est diam.", 
    "Etiam nec faucibus neque.",
    "Eu justo augue estas",
    "Mauris et rutrum felis."
];



/** 
 * Generates a random Lorem Ipsum paragraph
 * In: Number of statements
 * Out: String with requested 'In' Number of statements 
 * **/
function GenerateParagraph(stmt_num){
    var min = 0; 
    var max = rand_lorem_para.length - 1;  
    var para = "";
    // Populates Paragraph in a loop
    for(var i = 0; i < stmt_num; i++){
        var random = Math.floor(Math.random() * (+max - +min)) + +min;
        para += rand_lorem_para[random] + " ";
    }
    return para;
}



/** 
 * Generates a random Lorem Ipsum Title
 * In: Nothing
 * Out: Random Title
 * **/
function GenerateTitle(){
    var min = 0; 
    var max = rand_lorem_title.length - 1;  
    var random = Math.floor(Math.random() * (+max - +min)) + +min;
    return rand_lorem_title[random];
}



/** -------------------------------------  Labels ---------------------------------------- **/

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



/**       
 * Populates blocks from API into block_order
 * In:      BLOCK_QUEUE; a list (ordered) of the detected labels
 * Out:     block_order populated with adapted-names
 * Status:  Complete. This code my be redundant, inspect upon refactor period
 * TO BE IMPLEMENTED: 
 * =>  
 * **/
function Populate_blocks () {
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
