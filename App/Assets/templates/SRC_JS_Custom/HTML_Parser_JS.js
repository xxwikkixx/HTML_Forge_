/*

*/ 



/** Holds Order of detected blocks **/
var block_order= [];



/** Holds images used to randomly populate image placeholders on the site **/
var stock_images = [
"https://images.unsplash.com/photo-1553901753-215db344677a?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1651&q=80",
"https://images.unsplash.com/flagged/photo-1556669546-b1f29875df1c?ixlib=rb-1.2.1&auto=format&fit=crop&w=1650&q=80",
"https://images.unsplash.com/photo-1555985202-12975b0235dc?ixlib=rb-1.2.1&auto=format&fit=crop&w=1649&q=80",
"https://images.unsplash.com/photo-1555999017-0d0f80510719?ixlib=rb-1.2.1&auto=format&fit=crop&w=1650&q=80",
"https://images.unsplash.com/photo-1555999003-3f2bc447570e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjI0MX0&auto=format&fit=crop&w=1650&q=80",
"https://images.unsplash.com/photo-1554291499-563a504e0734?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjI0MX0&auto=format&fit=crop&w=1650&q=80",
"https://images.unsplash.com/photo-1555284023-249222086985?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1650&q=80",
"https://images.unsplash.com/photo-1554185256-7b994c659b88?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1616&q=80",
"https://images.unsplash.com/photo-1554558424-4a02a6451c4b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1646&q=80",
"https://images.unsplash.com/photo-1555381983-49b080e6ac89?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1525&q=80",
"https://images.unsplash.com/photo-1553901753-215db344677a?ixlib=rb-1.2.1&auto=format&fit=crop&w=1651&q=80",
"https://images.unsplash.com/photo-1553880376-2dec478c8e3b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1651&q=80",
"https://images.unsplash.com/photo-1551397954-fe3701bfb000?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1650&q=80",
"https://images.unsplash.com/photo-1551446591-142875a901a1?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1650&q=80",
"https://images.unsplash.com/photo-1550847067-93887e03cfbe?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1778&q=80",
"https://images.unsplash.com/photo-1550795658-d7d23cfaf9ee?ixlib=rb-1.2.1&auto=format&fit=crop&w=1275&q=80",
"https://images.unsplash.com/photo-1550640964-4775934de4af?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80",
"https://images.unsplash.com/photo-1550639264-38c3059c4620?ixlib=rb-1.2.1&auto=format&fit=crop&w=934&q=80",
"https://images.unsplash.com/photo-1549778003-d6c640bf6141?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=934&q=80",
"https://images.unsplash.com/photo-1549922470-949c45715199?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1300&q=80",
"https://images.unsplash.com/photo-1549945676-4fdf5f18a9fa?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=882&q=80",
"https://images.unsplash.com/photo-1550091840-165dc006661a?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=934&q=80",
"https://images.unsplash.com/photo-1549321682-36e2f8000f4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
"https://images.unsplash.com/photo-1513147122760-ad1d5bf68cdb?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1900&q=80",
"https://images.unsplash.com/photo-1519681393784-d120267933ba?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
"https://images.unsplash.com/photo-1548407260-da850faa41e3?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1787&q=80",
"https://images.unsplash.com/photo-1548560781-a7a07d9d33db?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=881&q=80",
"https://images.unsplash.com/photo-1548561711-73eae96ad48d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1796&q=80",
"https://images.unsplash.com/photo-1547974497-bb2a93b333ca?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=934&q=80",
"https://images.unsplash.com/photo-1547974996-050bf23b6196?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
"https://images.unsplash.com/photo-1548028052-a02d4402c2d3?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
"https://images.unsplash.com/photo-1547923933-994ec77aff2f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80",
"https://images.unsplash.com/photo-1547958600-915c8a5131de?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1951&q=80",
"https://images.unsplash.com/photo-1547950515-e652d0f50b1b?ixlib=rb-1.2.1&auto=format&fit=crop&w=934&q=80",
"https://images.unsplash.com/photo-1547882472-17b34a4465a2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
"https://images.unsplash.com/photo-1547810689-3c16713a7a3c?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1867&q=80",
"https://images.unsplash.com/photo-1547672920-7732a3b305be?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1868&q=80",
"https://images.unsplash.com/photo-1547634971-9a0b456745d8?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1850&q=80",
"https://images.unsplash.com/photo-1547634678-181c1103b6ba?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1850&q=80",
"https://images.unsplash.com/photo-1550572831-685fef460547?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=934&q=80",
"https://images.unsplash.com/photo-1547974497-bb2a93b333ca?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=934&q=80",
"https://images.unsplash.com/photo-1546720150-df94df154859?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1533&q=80",
"https://images.unsplash.com/photo-1546391811-f266bfa852ba?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
"https://images.unsplash.com/photo-1546417492-3f58b4f55148?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1868&q=80",
"https://images.unsplash.com/photo-1546260863-51e27ff43c68?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1234&q=80",
"https://images.unsplash.com/photo-1546258115-a6fe51f88baf?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1246&q=80",
"https://images.unsplash.com/photo-1545912629-40b1f3ba74ad?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1951&q=80",
"https://images.unsplash.com/photo-1545859537-922483c9cd75?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1947&q=80",
"https://images.unsplash.com/photo-1545851876-eb2bbc712ca6?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1275&q=80",
"https://images.unsplash.com/photo-1545852528-fa22f7fcd63e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1951&q=80",
"https://images.unsplash.com/photo-1545768076-c58b243b8f3e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1867&q=80",
"https://images.unsplash.com/photo-1545840893-d59d0bf89825?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1955&q=80",
"https://images.unsplash.com/photo-1545728779-fec7e3f92d27?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1871&q=80",
"https://images.unsplash.com/photo-1545750214-7685c8e77df5?ixlib=rb-1.2.1&auto=format&fit=crop&w=1234&q=80",
"https://images.unsplash.com/photo-1526749837599-b4eba9fd855e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80",
"https://images.unsplash.com/photo-1474524955719-b9f87c50ce47?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1952&q=80",
"https://images.unsplash.com/photo-1512092185028-631db13fbe52?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1285&q=80",
"https://images.unsplash.com/photo-1512488151-4d3098ed1107?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1234&q=80",
"https://images.unsplash.com/photo-1545362436-ca6b21bf4f68?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1234&q=80",
"https://images.unsplash.com/photo-1545335018-6c4f3536160a?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1867&q=80",
"https://images.unsplash.com/photo-1540050851371-6e1f12296cc8?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1300&q=80",
"https://images.unsplash.com/photo-1545063168-0e149bddf68c?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
"https://images.unsplash.com/photo-1545051522-b961890b306d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
"https://images.unsplash.com/photo-1544954617-f5c6b0d16164?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1932&q=80",
"https://images.unsplash.com/photo-1544961371-516024f8e267?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1234&q=80",
"https://images.unsplash.com/photo-1545022422-3ed8f20f8ec2?ixlib=rb-1.2.1&auto=format&fit=crop&w=1245&q=80",
"https://images.unsplash.com/photo-1544955242-521b5dad8507?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2000&q=80",
"https://images.unsplash.com/photo-1544604860-206456f08229?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
"https://images.unsplash.com/photo-1544738502-849ab3c63e50?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1927&q=80",
"https://images.unsplash.com/photo-1544718159-a2a2420b7e85?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
"https://images.unsplash.com/photo-1543663252-de9c18918fef?ixlib=rb-1.2.1&auto=format&fit=crop&w=1234&q=80",
"https://images.unsplash.com/photo-1544675113-8459426ad558?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2042&q=80",
"https://images.unsplash.com/photo-1473448912268-2022ce9509d8?ixlib=rb-1.2.1&auto=format&fit=crop&w=1925&q=80",
"https://images.unsplash.com/photo-1448518340475-e3c680e9b4be?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1951&q=80",
"https://images.unsplash.com/photo-1481126952208-cc3a6eaf68b5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1955&q=80",

];



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


/** 
 * Generates a random stock image 
 * In: Nothing
 * Out: Random Title
 * **/
function getImage(){
    var min = 0; 
    var max = stock_images.length - 1;  
    var random = Math.floor(Math.random() * (+max - +min)) + +min;
    return stock_images[random];
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

