// var UseLocalHost = false;


var host = "http://htmlforge.eastus.cloudapp.azure.com:8080";
// if(UseLocalHost)  host = "http://localhost:5000";


/** ------------------------------------- API CALLS ------------------------------------- **/
var API_BLOCK_CONVERT = host + "/api/startconvert";   // API that calls the AI
var API_BLOCK_REQ = host+ "/api/blocksdetected/";    // MUST ADD Session Id
var API_SESSION_ID = "ERROR";          // This gets populated by the API call from Upload.js
var API_URL = host;
var API_File_Uploaded = host + '/api/imageuploaded';
/** ------------------------------------------------------------------------------------- **/