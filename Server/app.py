from flask import Flask, abort, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)


@app.route('/')
def mainPage():
    return render_template('index.html')

@app.route('/processingpage')
def processingPage():
    return render_template('processingPage.html')

@app.route('/resultspage')
def resultsPage():
    return render_template('resultsPage.html')

@app.route('/uploadpage')
def uploadPage():
    return render_template('uploadPage.html')


UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file[]']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('upload_file'))
    return 'OK'



if __name__ == '__main__':
    app.run()
