import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from module.processing import total
import cv2

UPLOAD_FOLDER = '/home/viet/PycharmProjects/App/static/image_upload'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
img = '/home/viet/PycharmProjects/App/static/image_upload/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "Tuan"

result = []
name = 'NONE'   # ten anh goc
link1 = ''      # link anh goc
link2 = ''      # face
link3 = ''      # link anh detect


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    file = request.files['img_upload'] # lay link anh tu user
    if file and allowed_file(file.filename):
        global img, name
        file_name = 'user_img.jpg'  # name of user img will be saved in sever
        img = '{}{}'.format(img, file_name)

        print("NOOOOOOOOOOOOOO")    # test xem co luu anh moi upload len khong

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name)) # save user img to server
        name = file_name
        return redirect(url_for('result'))


@app.route('/result', methods=['GET', 'POST'])
def result():
    global link1, link2, link3, result, name
    link1 = 'static/image_upload/' + name    # link anh goc
    result = total(link1)    # ket qua tra ve
    link2 = 'static/image_detect/Photo.jpg'
    link3 = 'static/image_detect/Image_detected.jpg'
    #print("YYYYYYYYYYYYYYYYYYYYYY") # test xem anh co chay toi result.html khong

    return render_template('result.html', show_info=result, img1=link1, img2=link2, img3=link3)


if __name__ == "__main__":
    app.run(debug=True)