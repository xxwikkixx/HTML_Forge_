import os
import shutil
import socket

from PIL import Image
from flask import Flask, request, url_for, jsonify, send_file, json
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin

# Internal Classes
from BoxDetection import boxDetection
from CloudServiceConfig import flaskConfig

application = Flask(__name__)
application.debug = True
CORS(application, resources={r"/*": {"origins": "*"}})

if "local" in socket.getfqdn().lower():
    flaskConfig["serverAddress"] = "http://localhost:5000"
    print("The Server Is On Local")

userQue = []

@application.route('/')
@cross_origin(origin='*')
def mainPage():
    # dirc = os.path.dirname(os.path.realpath(__file__))
    # userUploadPath = os.path.join(dirc, "static")
    # shutil.rmtree(userUploadPath, ignore_errors=True)
    return "Server is up and running"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
UPLOAD_FOLDER = 'static'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@application.route('/upload', methods=['GET', 'POST', 'DELETE'])
@cross_origin(origin='*')
def upload_file():
    file = request.files['file']
    filename = secure_filename(file.filename)
    if request.method == 'POST':
        if not os.path.exists(os.path.join('static')):  # check if the folder exists
            os.makedirs(os.path.join('static'))  # make the static folder if it doesnt exist
        if file and allowed_file(file.filename):
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            # Image rotation
            picture = Image.open(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            width, height = picture.size
            if width> height:
                picture.rotate(270, expand=True).save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            imgPath = os.path.join(application.config['UPLOAD_FOLDER'], filename)
            job = boxDetection()
            job.setImagePath(imgPath)
            sessionID = job.getSessionID()
            userQue.append([job, sessionID])
            print ("UserQue", userQue)
            return sessionID
        else:
            return "File Extension not allowed"
    # DELETE doesnt work yet
    if request.method == 'DELETE':
        if os.path.exists(application.config['UPLOAD_FOLDER'] + filename):
            os.remove(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            return "File Delete"
    return 'ok'

@application.route('/upload/<ImageId>/Stock')
def uploadStock(ImageId):
    # if not os.path.exists(os.path.join('static')):  # check if the folder exists
    #     os.makedirs(os.path.join('static'))  # make the static folder if it doesnt exist
    picture = "Assets/templates/Images/Samples/Samp"+ImageId+".jpg"
    job = boxDetection()
    job.setImagePath(picture)
    userQue.append([job, job.getSessionID()])
    print ("UserQue", userQue)
    return json.dumps({"id": job.getSessionID()})


@application.route('/api/imageuploaded')
@cross_origin(origin='*')
def ApiImageUploadedReturn():
    filesInDir = []
    # dirc = os.path.dirname(os.path.realpath(__file__))
    # print(dirc) # prints 'C:....\HTML_Forge\application'
    # userUploadPath = os.path.join(dirc, "static")
    # print(userUploadPath) # prints "C:....\HTML_Forge\application\static''
    for root, dirs, files in os.walk(os.path.abspath("static")):
        for item in files:
            # print(item)
            filesInDir.append(item)
    filesURL = {}
    for i in filesInDir:
        filesURL.update({i: flaskConfig["serverAddress"] + url_for("static", filename=i)})

    return jsonify(ImageUpLoaded=filesURL)


@application.route('/api/startconvert/<usersession>')
@cross_origin(origin='*')
def convertRequest(usersession):
    # Search for session
    print(usersession)
    for i in userQue:
        print(i)
        if i[1] == usersession:
            print ("Start Session", usersession)
            sessionID, JSON_Path = i[0].startSession(i[0].getImagePath())
            print ("Start Session", "Done")
            userQue.remove(i)
            return jsonify(sessionID)
        else:
            print ("Job Not Found")
    return 'ok'


@application.route('/api/blocksdetected/getDebugImage/<usersession>')
@cross_origin(origin='*')
def getDebugImage(usersession):
    pid = 'UserUpload/' + usersession + "/" + usersession + ".jpg"
    return send_file(pid, mimetype='image/gif')


@application.route('/api/blocksdetected/<usersession>/CropImage/<filename>')
@cross_origin(origin='*')
def getCroppedImgage(usersession, filename):
    pid = 'UserUpload/' + usersession + "/ImageCrops/" + filename + ".png"
    return send_file(pid, mimetype='image/gif')


# accept the session ID into the URL to bring the data back for the specific user
@application.route('/api/blocksdetected/<usersession>')
@cross_origin(origin='*')
def ApiBlocksetectedReturn(usersession):
    dirc = "UserUpload/" + usersession + "/"
    for root, dirs, files in os.walk(dirc):
        for item in files:
            if item.endswith('.json'):
                path = os.path.join(root, item)
                jsonData = json.load(open(path))
                return jsonify(jsonData)
        for item in files:
            if (usersession + '.jpg') in item:
                path = os.path.join(root, item)
                return jsonify(debugImage=path)
    return 'ok'


# prettify the html string sent and return the URL back to the front end
@application.route('/api/html/<htmlstring>')
@cross_origin(origin='*')
def createHTMLFile(htmlstring):
    dirc = os.path.dirname(os.path.realpath(__file__))
    # print(dirc) # prints 'C:....\HTML_Forge\application'
    userUploadPath = os.path.join(dirc, "UserUpload")
    # print(userUploadPath) # prints "C:....\HTML_Forge\application\static''
    html_file = open(userUploadPath + "\htmlfile.html", "w")
    html_file.write(htmlstring)
    html_file.close()
    return send_file(userUploadPath + "\htmlfile.html", mimetype='text/html')

# Need to make a post request to send in a list and a number
@application.route('/api/parser', methods=['GET', 'POST'])
@cross_origin(origin='*')
def parser(list, num):
    for x in num:
        pass

if __name__ == '__main__':
    application.run(host='0.0.0.0')
