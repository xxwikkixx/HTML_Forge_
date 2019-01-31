from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def mainPage():
    return render_template('index.html')

@app.route('/processing')
def processingPage():
    return render_template('processingPage.html')

@app.route('/results')
def resultsPage():
    return render_template('resultsPage.html')

@app.route('/upload')
def uploadPage():
    return render_template('uploadPage.html')

if __name__ == '__main__':
    app.run()
