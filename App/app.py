import os
from flask import Flask, abort, render_template, request, redirect, url_for, jsonify, send_file, send_from_directory, make_response, session
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
# Internal Classes
from OpenCVBoxDetection import startSession

app = Flask(__name__)
app.debug = True
cors = CORS(app)


@app.route('/')
def mainPage():
    startSession('Sample Images/S_1.jpg')
    return "Server OK"
    # return render_template('LandingPage.html')


def detectBrowser():
    browser = request.user_agent.browser
    version = request.user_agent.version and int(request.user_agent.version.split('.')[0])
    platform = request.user_agent.platform
    uas = request.user_agent.string
    return browser + platform + uas



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods = ['GET', 'POST', 'DELETE'])
def upload_file():
    file = request.files['file']
    filename = secure_filename(file.filename)
    if request.method == 'POST':
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify(imageUpload = url_for('upload_file', filename=filename))
        else:
            return "File Extension not allowed"

    if request.method == 'DELETE':
        if os.path.exists(UPLOAD_FOLDER + filename):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "File Delete"
    return 'ok'


@app.route('/api/imageuploaded')
def ApiImageUploadedReturn():
#     get the image path from the folder
#     connect it with the URL to output the image
    filesInDir = []
    for root, dirs, files in os.walk(os.path.abspath("static")):
        for item in files:
            # print(item)
            filesInDir.append(item)

    filesURL = {}
    for i in filesInDir:
        filesURL.update({i:'http://localhost:5000' + url_for("static", filename= i)})
    return jsonify(ImageUpLoaded= filesURL)


@app.route('/api/blocksdetected')
def ApiBlocksetectedReturn():
    return 'OK'

if __name__ == '__main__':
    app.run(threaded=True)

