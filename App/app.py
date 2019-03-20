import os

import cv2
from flask import Flask, abort, render_template, request, redirect, url_for, jsonify, send_file, send_from_directory, \
    make_response, session, json
from sphinx.util import requests
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
# Internal Classes
from OpenCVBoxDetection import startSession, initializeSession

app = Flask(__name__)
app.debug = True
cors = CORS(app)

session = ''
imgPath = ''


# @app.route('/')
# def mainPage(img):
#     global session
#     sessionID, JSON_Path = startSession(img)
#     session = sessionID
#     return jsonify("Session ID : " + sessionID + "</br> JSON Path: " + JSON_Path)
#     # return render_template('LandingPage.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload', methods=['GET', 'POST', 'DELETE'])
def upload_file():
    global imgPath
    file = request.files['file']
    filename = secure_filename(file.filename)
    if request.method == 'POST':
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            imgPath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(imgPath)
            sess = initializeSession()
            # print(sess)
            return sess
        else:
            return "File Extension not allowed"
    # DELETE doesnt work yet
    if request.method == 'DELETE':
        if os.path.exists(UPLOAD_FOLDER + filename):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "File Delete"
    return 'ok'


@app.route('/api/imageuploaded')
def ApiImageUploadedReturn():
    filesInDir = []
    for root, dirs, files in os.walk(os.path.abspath("static")):
        for item in files:
            # print(item)
            filesInDir.append(item)

    filesURL = {}
    for i in filesInDir:
        filesURL.update({i: 'http://localhost:5000' + url_for("static", filename=i)})
    return jsonify(ImageUpLoaded=filesURL)


@app.route('/api/startconvert')
def convertRequest():
    global session
    sessionID, JSON_Path = startSession(imgPath)
    session = sessionID
    return jsonify(sessionID)


@app.route('/api/blocksdetected/getDebugImage/<usersession>')
def getDebugImage(usersession):
    pid = 'UserUpload/' + usersession + "/" + usersession + ".jpg"
    return send_file(pid, mimetype='image/gif')


@app.route('/api/blocksdetected/<usersession>/CropImage/<filename>')
def getCroppedImgage(usersession, filename):
    pid = 'UserUpload/' + usersession + "/ImageCrops/" + filename + ".png"
    return send_file(pid, mimetype='image/gif')


# accept the session ID into the URL to bring the data back for the specific user
@app.route('/api/blocksdetected/<usersession>')
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


def moifyJson(usersession):
    dirc = os.path.dirname(os.path.realpath(__file__))
    userUploadPath = os.path.join(dirc, "UserUpload")
    jsonPath = os.path.join(userUploadPath, usersession)
    dict = []
    with open(os.path.join(jsonPath, 'data.json'), 'r') as f:
        jsonData = json.load(f)
        jsData = jsonData["blocks"]
        for i in jsData:
            resp = i["Image_Crop_Path"]
            for pths in resp:
                print(resp)

if __name__ == '__main__':
    app.run(threaded=True)
