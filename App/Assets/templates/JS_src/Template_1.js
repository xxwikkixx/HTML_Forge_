/*  This JavaScript file is responsible for the production of all Template 1 Code
 *
 *      INPUT:      An array 'blocks' is passed into the _makeHTML function of this template
 *      OUTPUT:     The _makeHTML function returns code for the desired template
 *      Note:       All functions in this file with the exception of _makeHTML are helper functions
 */



/**  
 * Generates HTML code for a Basic Template Initialization 
 * In:      Nothing
 * Out:     returns code for a header
 * Status:  Functional, improvements pending.
 * TO BE IMPLEMENTED: 
 * =>  INPUT CSS Source based on theme 
 * =>  Title based on api
 * **/
function T1_init () {

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
function T1_init_End () {

    var codeBuffer = "";

    codeBuffer += '</body>';
    codeBuffer += '</html>';

    return codeBuffer;
}



/**      
 * Generates Wrapper HTML Code for 'section' segment within the body
 * In:      Nothing
 * Out:     Returns code for begining segment
 * Status:  COMPLETE
 * **/
function T1_ContainerTop () {
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
function T1_ContainerBot () {
    var codeBuffer = "";
    codeBuffer +=   '</div>';
    codeBuffer += '</div>';
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
function T1_Header (link_num) {

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
function T1_Footer () {

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
function T1_Para () {

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
function T1_Title () {

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
function T1_SingleImage () {

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
function T1_ImagePara () {

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
function T1_ImagePrev () {

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
function T1_ImageSimple () {

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
function T1_ImgLeft_TxtRight () {

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
function T1_ImgRight_TxtLeft () {

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
function T1_ImgTop_TxtBottom () {

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
 * Generates HTML for the Basic Template 
 * In:      Blocks
 * Out:     HTML Code for all blocks passed, formatted into Basic Template
 * Status:  COMPLETE.
 * **/
function T1_MakeHTML (blocks) {

    var code = "";              // Code will be appended to this through the process
    var head_count = 0;         // Will keep count of headers found
    var foot_count = 0;         // Will keep count of footers found

    // Scan for Headers and Footers, we will not allow duplicates by force.
    for(var i = 0; i < blocks.length; i++){
        if(blocks[i] == 'label_1') {head_count++;}
        if(blocks[i] == 'label_2') {foot_count++;}
    }
    
    // Initalizes HTML
    code += T1_init ();
    
    // Header Exclusive, this forces a header to always be placed on top regardless
    // of the location it was found
    if(head_count > 0){code += T1_Header(); head_count--;}

    // Container Open (Used only for the basic Template)
    code += T1_ContainerTop();

    // Loop through blocks and output code as necessary 
    for(var i = 0; i < blocks.length; i++){

      if (blocks[i] == 'label_1')   {   // Special conditions for headers
          if(head_count > 0) {          // ONLY pushes alternate code if header was used
              code += T1_Title();
              head_count--;
            }}     

      if (blocks[i] == 'label_2')   {   // Special conditions for footers
          if(foot_count > 1) {          // ONLY pushed alternate code if footer was detected
              code += T1_Title();
              foot_count--;
            }}

      // All Other Labels
      if (blocks[i] == 'label_3')   {code += T1_Para();}
      if (blocks[i] == 'label_4')   {code += T1_Title();}
      if (blocks[i] == 'label_5')   {code += T1_SingleImage();}
      if (blocks[i] == 'label_6')   {code += T1_ImagePara();}
      if (blocks[i] == 'label_7')   {code += T1_ImagePrev();}
      if (blocks[i] == 'label_8')   {code += T1_ImageSimple();}
      if (blocks[i] == 'label_9')   {code += T1_ImgLeft_TxtRight();}
      if (blocks[i] == 'label_10')  {code += T1_ImgRight_TxtLeft();}
      if (blocks[i] == 'label_11')  {code += T1_ImgTop_TxtBottom();}
    }

    // Container Close (Used only for the basic Template)
    code += T1_ContainerBot ();
    
    // Footer Exclusive, forces a detected footer to always place on the bottom 
    // regardless of the location it was found
    if(foot_count > 0){code += T1_Footer();}

    // Closes initalized HTML
    code += T1_init_End();
    
    code = formatFactory(code);
    return code;
}
