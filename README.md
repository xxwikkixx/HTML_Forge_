# HTML_Forge

## Todo
- [ ] More AI training
- [ ] Improve Front-End UI 
- [ ] Web Editor and Viewer
- [ ] Output Code Beautifier


## Description
HTML Forge is a Web-Based application that converts a Graphical User Interface (GUI) mockup into HTML5 code by leveraging the power of Machine Learning. The process of converting a GUI into code is generally the responsibility of developers. The process itself is time-consuming and prevents developers from allocating their time to more time-demanding issues such as implementing logic and functionality into an application. HTML Forge is designed to speed up work-flow, and allows developers and students alike to speed up their web development tasks by simplifying the process into a simple upload and convert button.
  
## How It Works
Front-End supports beautiful and responsive UI for the user to upload their images, edit detected building blocks, and HTML code constructor.  
In Back-End, Since Google's AutoML API doesn't support localization and multi-object detection. The user upload image has to feed through OpenCV algorithm for pre-processing. The OpenCV algorithm will crop all the detected blocks into separate images. Then sends all the cropped images to AutoML for image classification. Once the image return from Google with predictions, The information is pass to front-end as JSON for constructing the output website.

## Installation
#### Built with
Flask, Google Automl, OpenCV  
#### Dependencies
Important Dependencies installations may required.  
```Flask, google-api-core, google-auth, numpy, matplotlib, Pillow, cv2```  
Full requirements and dependencies can be found in [requirements.txt](https://github.com/adwuard/HTML_Forge/blob/master/App/requirements.txt) file

## Configure and connect to your AutoML Model
```python
# CloudServiceConfig.py
conf = {
    "project_id": "htmlforge", # Project ID on Google AutoML Cloud Service
    "compute_region": "us-central1",
    "model_id": "ICN8414522955192401378", #ID to the trained model
    "service_API_Path": "PATH/TO/API_CREDENTIAL.json" # Google API Credentials
}
```

## Usage
Run App.py with Flask to start the application. You will then be able to access it at localhost:5000.
Then open the AppPage.html in browser to use the software in local host.

## Authors
[Hsuan Han Lai](https://github.com/adwuard)   
[Waqas A Latif](https://github.com/xxwikkixx)  
[Khalid Kmq Qubbaj](https://github.com/khalkmq)  

## License
This project is under. Please read here [MIT License.](https://github.com/adwuard/HTML_Forge/blob/master/LICENSE)
