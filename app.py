import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/viet/PycharmProjects/App/static/image'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
img = '/home/viet/PycharmProjects/App/static/image/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "Viet Anh"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file and allowed_file(file.filename):
            global img
            filename = secure_filename(file.filename)
            img = '{}{}'.format(img, filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # ham xu ly anh
    return '''
    <!doctype html>
    <title>Upload Image</title>
    <h1>Upload images</h1>
    <form method=post enctype=multipart/form-data>
        <input type=file name=file>
            <input type=submit value=Upload>
            <a href="upload.html"><button>go</button</a>
    </form>
    '''


@app.route('/')
def hello():
    return "hello"


if __name__ == "__main__":
    app.run(debug=True)