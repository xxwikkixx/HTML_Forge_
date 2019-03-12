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
        url: 'http://localhost:5000',
        process: {
            url: '/upload',
            onload: (response) => {
                console.log(response)
                // window.location.href='http://google.com'
            }
        }
    }
});