/*
We want to preview images, so we need to register the Image Preview plugin
*/
FilePond.registerPlugin(
	
	// encodes the file as base64 data
  FilePondPluginFileEncode,
	
	// validates the size of the file
	FilePondPluginFileValidateSize,
	
	// corrects mobile image orientation
	FilePondPluginImageExifOrientation,
	
	// previews dropped images
  FilePondPluginImagePreview
);


// Select the file input and use create() to turn it into a pond
FilePond.create(
	document.querySelector('input')
);

FilePond.setOptions({
  server: {
      url: 'http://htmlforge-dev4.us-east-1.elasticbeanstalk.com',
      process: {
          url: '/upload',
          method: 'POST',
          onload: (response) => {
              //console.log(response);
              API_SESSION_ID = response;
              //document.getElementById("confirm_button" ).style.display = "block";     // Shows
              $('#confirm_button').prop('disabled', false);        // Allows button to be pressed
              imageJSON()
              // window.location.href='http://google.com'
          }
      },
      revert:{
          url: '/upload',
          method: 'DELETE',
          onload: (response) => {
              // console.log(response)
              // window.location.href='http://google.com'
          }
      }
  }
});


function imageJSON(){
    fetch('http://htmlforge-dev4.us-east-1.elasticbeanstalk.com/api/imageuploaded')
        .then(function (response) {
            return response.json()
        })
        .then(data =>{

            console.log("Data"+data);
        })
}