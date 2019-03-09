import os
import json
from flask import Flask, abort, render_template, request, redirect, url_for, jsonify, send_file, send_from_directory, make_response, session
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin



app = Flask(__name__)
cors = CORS(app)


@app.route('/')
def mainPage():
    # if not request.cookies.get(detectBrowser()):
    #     res = make_response("Cookies")
    #     res.set_cookie(detectBrowser(), os.urandom(16), max_age=60*60*24*365*2)
    # else:
    #     make_response(request.cookies.get(detectBrowser()))
    #     print("cookies found")
    return "Server OK"
    # return render_template('LandingPage.html')

# @app.route('/apppage')
# def processingPage():
#     return render_template('AppPage.html')

# @app.route('/uploadpage')
# def uploadPage():
#     return render_template('uploadPage.html')
#

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
UPLOAD_FOLDER = 'Assets/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify(name=filename)
        else:
            return "File Extension not allowed"
    return 'ok'


@app.route('/api/imageuploaded', methods = ['GET'])
def ApiImageUploadedReturn():
#     get the image path from the folder
#     connect it with the URL to output the image
    data = {}
    data['imageUploaded'] = 2
    json_data = json.dumps(data)
    print(json_data)
    return json_data


if __name__ == '__main__':
    app.run()

