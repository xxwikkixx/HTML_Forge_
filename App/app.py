from flask import Flask, abort, render_template, request, redirect, url_for, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import json


app = Flask(__name__)


@app.route('/')
def mainPage():
    return render_template('LandingPage.html')

@app.route('/apppage')
def processingPage():
    return render_template('AppPage.html')

@app.route('/uploadpage')
def uploadPage():
    return render_template('uploadPage.html')



# https://github.com/ngoduykhanh/flask-file-uploader
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
UPLOAD_FOLDER = 'Uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file[]']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'OK'
        else:
            return "File Extension not allowed"
    return redirect(url_for('upload'))


# uploaded image views
# all blocks detected from google
# passing the list of blocks to the interpreter for conversion
# display the returned converted code

def add():
    return 2+2

@app.route('/api/imageuploaded', methods = ['GET'])
def ApiImageUploadedReturn():
#     get the image path from the folder
#     connect it with the URL to output the image
    data = {}
    data['imageUploaded'] = add()
    json_data = json.dumps(data)
    print(json_data)
    return json_data




if __name__ == '__main__':
    app.run()



# https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
