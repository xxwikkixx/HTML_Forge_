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



/**  
 * Generates HTML code for a Basic Template Initialization 
 * In:      Nothing
 * Out:     returns code for a header
 * Status:  Functional, improvements pending.
 * TO BE IMPLEMENTED: 
 * =>  INPUT CSS Source based on theme 
 * =>  Title based on api
 * **/
function BasicTemplate_init () {

    var codeBuffer = "";

    codeBuffer += '<!DOCTYPE html>';
    codeBuffer += '<html lang="en">';
    codeBuffer +=   '<head>';
    codeBuffer +=   '<title>Generated Site</title>';
    codeBuffer +=   '<meta charset="UTF-8">';
    codeBuffer +=   '<link rel="stylesheet" href="layout.css" type="text/css">'
    codeBuffer += '</head>';
    codeBuffer += '<body>';

    return codeBuffer;
}



/** 
 * Generates HTML code for a Basic Template Closing Statements
 * In:      Nothing
 * Out:     Returns code for closing statements
 * Status:  COMPLETE
 * **/
function BasicTemplate_init_End () {

    var codeBuffer = "";

    codeBuffer += '</body>';
    codeBuffer += '</html>';

    return codeBuffer;
}



/**                LABEL 1: HEADER
 * Generates HTML code for a basic Template Header
 * In:      Number of links in bar
 * Out:     Returns code for a header
 * Status:  Functional, improvements pending.
 * TO BE IMPLEMENTED: 
 * =>  INPUT Name of Website if detected by OCR
 * =>  INPUT Motto if detected by OCR
 * =>  INPUT Text-link names if detected by OCR
 * **/
function BasicTemplate_Header (link_num) {

    var codeBuffer = "";

    codeBuffer += '<div class="wrapper row1">';
    codeBuffer +=   '<header id="header" class="clear">';
    codeBuffer +=       '<div id="hgroup">';
    codeBuffer +=           '<h1><a href="#">Generated Website</a></h1>';
    codeBuffer +=           '<h2>Your Motto Goes Here</h2>';
    codeBuffer +=       '</div>';
    codeBuffer +=       '<nav>';
    codeBuffer +=           '<ul>';
    
    // Populate links as neccessary
    for(var i = 0; i < link_num - 1; i++){
    codeBuffer +=               '<li><a href="#">Text Link</a></li>';
    }

    // Force minimum one link for CSS.
    codeBuffer +=               '<li class="last"><a href="#">Text Link</a></li>';

    codeBuffer +=  '</ul></nav></header></div>';
 
    return codeBuffer;
}



/**                LABEL 2: FOOTER
 * Generates HTML code for a basic Template Footer
 * In:      Nothing
 * Out:     Returns code for a footer
 * Status:  Functional, improvements pending.
 * TO BE IMPLEMENTED: 
 * =>  INPUT text detected by OCR
 * **/
function BasicTemplate_Footer () {

    var codeBuffer = "";

    codeBuffer += '<div class="wrapper row3">';
    codeBuffer +=   '<footer id="footer" class="clear">';
    codeBuffer +=       '<p class="fl_left">' + GenerateTitle() + '<a href="#">' + GenerateTitle() + '</a></p>';       
    codeBuffer +=       '<p class="fl_right">' + GenerateTitle() + '<a target="_blank" href="#">' + GenerateTitle() + '</a></p>';          
    codeBuffer +=   '</footer>';           
    codeBuffer += '</div>';       

    return codeBuffer;
}



/**                LABEL 3: Paragraph
 * Generates HTML code for a basic paragraph section
 * In:      Nothing
 * Out:     Returns code for a paragraph section
 * Status:  Functional, improvements pending.
 * TO BE IMPLEMENTED: 
 * =>  INPUT text detected by OCR
 * **/
function BasicTemplate_Para () {

    var codeBuffer = "";

    codeBuffer += '<section id="shout">';
    codeBuffer +=   '<h2>' + GenerateTitle() + '</h2>';
    codeBuffer +=   '<p>' + GenerateParagraph(6) + '</p>';
    codeBuffer += '</section>';

    return codeBuffer;
}



/**                LABEL 4: Title
 * Generates HTML code for a single Title
 * In:      Nothing
 * Out:     Returns code for a Title
 * Status:  Functional, improvements pending.
 * TO BE IMPLEMENTED: 
 * =>  INPUT text detected by OCR
 * **/
function BasicTemplate_Title () {

    var codeBuffer = "";    

    codeBuffer += '<section id="shout">';
    codeBuffer +=   '<h2>' + GenerateTitle() + '</h2>';
    codeBuffer += '</section>';

    return codeBuffer;
}



/**             LABEL 5: Image Single
 * Generates HTML code for Single Image
 * In:      Nothing
 * Out:     Returns code for an Image
 * Status:  Functional, improvements pending.
 * TO BE IMPLEMENTED: 
 * =>  Image populated from theme choice
 * **/
function BasicTemplate_SingleImage () {

    var codeBuffer = "";
    codeBuffer += '<section id="slider">';
    codeBuffer +=   '<a href="#">';
    codeBuffer +=       '<img src="Blank-grey.gif" alt="" style="width: 960px; height: 360px;">';
    codeBuffer +=   '</a>';
    codeBuffer += '</section>';

    return codeBuffer;
}



/**            LABEL 6: Image Parrallax
 * Generates HTML code for Parralax Image
 * In:      Nothing
 * Out:     Returns code for HTML portion of a Parallax Image
 * Status:  Functional, improvements pending.
 * TO BE IMPLEMENTED: 
 * =>  Image populated from theme choice
 * =>  Java Script fixed with new CSS
 * **/
function BasicTemplate_ImagePara () {

    var codeBuffer = "";
    codeBuffer += '<section id="slider">';
    codeBuffer +=   '<a href="#">';
    codeBuffer +=       '<img src="Arrow_L.png" alt="" style="width: 130px; height: 360px;">';
    codeBuffer +=       '<img src="Blank-grey.gif" alt="" style="width: 690px; height: 360px;">';
    codeBuffer +=       '<img src="Arrow_R.png" alt="" style="width: 130px; height: 360px;">';
    codeBuffer +=   '</a>';
    codeBuffer += '</section>';

    return codeBuffer;
}



/**             LABEL 7: Image Preview
 * Generates HTML code for Image Preview
 * In:      Nothing
 * Out:     Returns code for an Image
 * Status:  INCOMPLETE, improvements pending.
 * TO BE IMPLEMENTED: 
 * =>  Image populated from theme choice
 * =>  Incorrect Layout? Fix CSS
 * **/
function BasicTemplate_ImagePrev () {

    var codeBuffer = "";
    codeBuffer += '<section id="slider">';
    codeBuffer +=   '<a href="#">';
    codeBuffer +=       '<img src="Blank-grey.gif" alt="" style="width: 960px; height: 360px;">';
    codeBuffer +=   '</a>';
    codeBuffer += '</section>';
    codeBuffer += '<section id="latest" class="last clear">';
    
    for (var i = 0; i < 3; i++){
        codeBuffer += '<article class="one_quarter">';
        codeBuffer +=   '<figure><img src="Blank-grey.gif" width="215" height="100" alt=""></figure>';
        codeBuffer += '</article>';
    }
    
    codeBuffer += '<article class="one_quarter lastbox">';
    codeBuffer +=   '<figure><img src="Blank-grey.gif" width="215" height="100" alt=""></figure>';
    codeBuffer += '</article>';

    codeBuffer += '</section>';
    
    return codeBuffer;
}



/**             LABEL 8: Image Simple
 * Generates HTML code for a simple image gallary
 * In:      Nothing
 * Out:     Returns code for a simple image gallary
 * Status:  INCOMPLETE, improvements pending.
 * TO BE IMPLEMENTED: 
 * =>  INPUT text detected by OCR
 * **/
function BasicTemplate_ImageSimple () {

    var codeBuffer = "";

    for(var x = 0; x < 3; x++){
        codeBuffer += '<section id="latest" class="last clear">';
        for(var i = 0; i < 4; i++){
            if(i < 3) {codeBuffer += '<article class="one_quarter">';}
            else      {codeBuffer += '<article class="one_quarter lastbox">';}
            codeBuffer +=   '<figure><img src="Blank-grey.gif" width="215" height="100" alt="">';
            codeBuffer +=      '<figcaption>';
            codeBuffer +=           '<h2>' + GenerateTitle() + '</h2>';
            codeBuffer +=           '<p>'  + GenerateParagraph(2) + '</p>';
            codeBuffer +=      '</figcaption>';
            codeBuffer +=   '</figure>';
            codeBuffer += '</article>';
        }
        codeBuffer += '</section>';
    }

    return codeBuffer;
}



/**       LABEL 9: Image Left Text Right
 * Generates HTML code for image_left text_right
 * In:      Nothing
 * Out:     Returns code for image_left text_right
 * Status:  Functional, improvements pending.
 * TO BE IMPLEMENTED: 
 * =>  INPUT text detected by OCR
 * =>  Image populated from random theme array
 * **/
function BasicTemplate_ImgLeft_TxtRight () {

    var codeBuffer = "";

    codeBuffer += '<section id="imgLTxtR" class="clear">';
    codeBuffer +=   '<figure><img src="Blank-grey.gif" alt="">';
    codeBuffer +=       '<figcaption>';
    codeBuffer +=           '<h2>' + GenerateTitle() + '</h2>';
    codeBuffer +=           '<p>' + GenerateParagraph(5) + '</p>';
    codeBuffer +=       '</figcaption>';
    codeBuffer +=   '</figure>';
    codeBuffer += '</section>';

    return codeBuffer;
}



/**       LABEL 10: Image Right Text Left
 * Generates HTML code for image_right text_left
 * In:      Nothing
 * Out:     Returns code for image_right text_left
 * Status:  Functional, improvements pending.
 * TO BE IMPLEMENTED: 
 * =>  INPUT text detected by OCR
 * **/
function BasicTemplate_ImgRight_TxtLeft () {

    var codeBuffer = "";

    codeBuffer += '<section id="imgRTxtL" class="clear">';
    codeBuffer +=   '<figure><img src="Blank-grey.gif" alt="">';
    codeBuffer +=       '<figcaption>';
    codeBuffer +=           '<h2>' + GenerateTitle() + '</h2>';
    codeBuffer +=           '<p>' + GenerateParagraph(5) + '</p>';
    codeBuffer +=       '</figcaption>';
    codeBuffer +=   '</figure>';
    codeBuffer += '</section>';

    return codeBuffer;
}



/**       LABEL 11: Image Top Text Bottom
 * Generates HTML code for Image Top text Bottom
 * In:      Nothing
 * Out:     Returns code for Image Top text Bottom
 * Status:  Functional, improvements pending.
 * TO BE IMPLEMENTED: 
 * =>  INPUT text detected by OCR
 * **/
function BasicTemplate_ImgTop_TxtBottom () {

    var codeBuffer = "";

    codeBuffer +=  '<section id="imgTTxtB" class="clear">';
    codeBuffer +=    '<figure><img src="Blank-grey.gif" alt="">'; 
    codeBuffer +=      '<figcaption>';
    codeBuffer +=         '<h2>' + GenerateTitle() + '</h2>';
    codeBuffer +=         '<p>'  + GenerateParagraph(7) + '</p>';
    codeBuffer +=      '</figcaption>';
    codeBuffer +=    '</figure>';
    codeBuffer +=  '</section>';

    return codeBuffer;
}



/**      
 * Generates Wrapper HTML Code for 'section' segment within the body
 * In:      Nothing
 * Out:     Returns code for begining segment
 * Status:  COMPLETE
 * **/
function BasicTemplate_ContainerTop () {
    var codeBuffer = "";
    codeBuffer += '<div class="wrapper row2">';
    codeBuffer +=   '<div id="container" class="clear">';
    return codeBuffer;
}



/**      
 * Generates Wrapper HTML Code for 'section' segment within the body
 * In:      Nothing
 * Out:     Returns code for ending segment
 * Status:  COMPLETE
 * **/
function BasicTemplate_ContainerBot () {
    var codeBuffer = "";
    codeBuffer +=   '</div>';
    codeBuffer += '</div>';
    return codeBuffer;
}



/**       
 * Populates blocks from API into block_order
 * In:      API Call
 * Out:     Nothing
 * Status:  WAITING ON API RETREIVAL 
 * TO BE IMPLEMENTED: 
 * =>  
 * **/
function Populate_blocks () {

    labelAdapter();

    // block_order.push('label_1');
    // block_order.push('label_3');    // Paragraph
    // block_order.push('label_4');    // Title
    // block_order.push('label_5');    // One image
    // block_order.push('label_6');    // Image Banner (Slider)
    // block_order.push('label_7');    // Image Preview
    // block_order.push('label_8');    // Image Gallary
    // block_order.push('label_9');    // Text Right Image Left
    // block_order.push('label_10');   // Text Left Image RIght
    // block_order.push('label_11');   // Text Bot Image Top
    // block_order.push('label_2');

}



/**       
 * Populates blocks from API into block_order
 * In:      Blocks
 * Out:     Nothing
 * Status:  
 * TO BE IMPLEMENTED: 
 * =>  
 * **/
function make_HTML_Basic (blocks) {

    var code = "";
    var head_found = false;
    var foot_found = false;
    var head_count = 0;
    var foot_count = 0;

    // Scan for Headers and Footers, we will not allow duplicates by force.
    for(var i = 0; i < blocks.length; i++){
        if(blocks[i] == 'label_1') {head_found = true; head_count++;}
        if(blocks[i] == 'label_2') {foot_found = true; foot_count++;}
    }
    
    // Initalizes HTML
    code += BasicTemplate_init ();
    
    // Header Exclusive, this forces a header to always be placed on top regardless
    // of the location it was found
    if(head_found){code += BasicTemplate_Header(); head_count--;}

    // Container Open (Used only for the basic Template)
    code += BasicTemplate_ContainerTop();


    // Loop through blocks and output code as necessary 
    for(var i = 0; i < blocks.length; i++){

      if (blocks[i] == 'label_1')   {   // Special conditions for headers
          if(head_count > 0) {          // ONLY pushes alternate code if header was used
              code += BasicTemplate_Title();
              head_count--;
            }}     

      if (blocks[i] == 'label_2')   {   // Special conditions for footers
          if(foot_count > 1) {          // ONLY pushed alternate code if footer was detected
              code += BasicTemplate_Title();
              foot_count--;
            }}

      // All Other Labels
      if (blocks[i] == 'label_3')   {code += BasicTemplate_Para();}
      if (blocks[i] == 'label_4')   {code += BasicTemplate_Title();}
      if (blocks[i] == 'label_5')   {code += BasicTemplate_SingleImage();}
      if (blocks[i] == 'label_6')   {code += BasicTemplate_ImagePara();}
      if (blocks[i] == 'label_7')   {code += BasicTemplate_ImagePrev();}
      if (blocks[i] == 'label_8')   {code += BasicTemplate_ImageSimple();}
      if (blocks[i] == 'label_9')   {code += BasicTemplate_ImgLeft_TxtRight();}
      if (blocks[i] == 'label_10')  {code += BasicTemplate_ImgRight_TxtLeft();}
      if (blocks[i] == 'label_11')  {code += BasicTemplate_ImgTop_TxtBottom();}
    }

    // Container Close (Used only for the basic Template)
    code += BasicTemplate_ContainerBot ();
    
    // Footer Exclusive, forces a detected footer to always place on the bottom 
    // regardless of the location it was found
    if(foot_found){code += BasicTemplate_Footer();}

    // Closes initalized HTML
    code += BasicTemplate_init_End();

    return code;
}


// Populate_blocks();
// console.log(make_HTML_Basic(block_order));