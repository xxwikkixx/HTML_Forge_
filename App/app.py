from flask import Flask, abort, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename


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
UPLOAD_FOLDER = 'uploads/'
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



if __name__ == '__main__':
    app.run()



# https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
