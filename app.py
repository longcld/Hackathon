import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import pytesseract, cv2

UPLOAD_FOLDER = '/home/healer/PycharmProjects/hackathon/static/image'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
img = '/home/healer/PycharmProjects/hackathon/static/image/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "Tuan"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/show_info', methods=['GET', 'POST'])
def upload_file():
    check = 'no'
    list = []
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['file_upload']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file and allowed_file(file.filename):
            global img
            file_name = secure_filename(file.filename)
            img = '{}{}'.format(img, file_name)
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
            check = 'yes'
            list = ['tuan', '123', '567']
            link = file_name
            print(link)
            # ham xu ly anh
    return render_template('show_info.html', show_more = check, show_info = list, link_img = link)

if __name__ == "__main__":
    app.run(debug=True)
