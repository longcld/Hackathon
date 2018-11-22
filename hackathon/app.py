import os
from flask import Flask, request, redirect, url_for, render_template
from module.processing import get_info, add_data, check_exsist, check_form

UPLOAD_FOLDER = '/home/healer/PycharmProjects/hackathon/static/image_upload'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
img = '/home/healer/PycharmProjects/hackathon/static/image_upload/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

result = []     # result after detecting image to string
name = ''       # name of user's image
link1 = ''      # link user's image
link2 = ''      # link user's face image
link3 = ''      # link image after processing
ID = ''         # user's ID when sign_in
home = 'Yes'    # no printing user's error

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
    return render_template('home.html', check=home)

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    file = request.files['img_upload']      # get link user's image from user's computer
    if file and allowed_file(file.filename):
        global img, name
        name = 'user_img.jpg'  # name user's image is saved in server
        img = '{}{}'.format(img, name)     # link user's image which is saved in server

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], name)) # save user's image to server
        return redirect(url_for('result'))

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    global ID
    ID = request.form['search'] # text box
    return redirect(url_for('result'))

@app.route('/result', methods=['GET', 'POST'])
def result():
    global link1, link2, link3, result, name, ID, home
    link1 = ''
    link2 = ''
    link3 = ''
    check = False
    if ID=='':  # sign_up
        link1 = 'static/image_upload/' + name   # link user's image in image_upload
        result = get_info(link1)    # result after detecting image to string
        link2 = 'static/image_detect/Photo.jpg' # link user's face image in image_detect
        link3 = 'static/image_detect/Image_detected.jpg'    # link image after processing
        add_data(result)    # add data to database
        check = True
    else:   # sign_in
        ID = ID.upper()
        if check_form(ID):  # check ID from form
            result = check_exsist(ID)   # search ID in database
            if result != []:
                link2 = 'static/image_data/{}.jpg'.format(ID)   # link user's face image in image_data
                check = True

    if check:
        home = 'Yes'    # when sign_in success or sign_up, reset home to avoid printing user's error
        ID = ''     # reset ID to avoid blocking sign_up
        return render_template('result.html', show_info=result, img1=link1, img2=link2, img3=link3)

    home = 'No' # when sign_in fail, print user's error
    ID = '' # reset ID to avoid blocking sign_up
    return render_template('home.html', check=home)

if __name__ == "__main__":
    app.run(debug=True)