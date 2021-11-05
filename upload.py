from __main__ import app
import os
from flask import request, redirect, send_file
from flask.templating import render_template
from numpy.lib.npyio import save
from werkzeug.utils import secure_filename
from tools.object_detection import detection_video

UPLOAD_FOLDER = './static/assets/video'
ALLOWED_EXTENSIONS = {'3gp', 'mp4', 'ogg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) # get secured filename

            file_ex = filename.rsplit('.', 1)[1].lower() # get extention file
            re_filename = 'video.'+file_ex 

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename); 
            file.save(filepath)

            re_filepath = os.path.join(app.config['UPLOAD_FOLDER'], re_filename); 
            os.rename(filepath, re_filepath) # rename file

            filepath_output = os.path.join(app.config['UPLOAD_FOLDER'], 'output.avi')
            detection_video(filename=re_filepath, save2=filepath_output)
            return render_template('pages/index.html', filename=re_filename)

    return render_template('pages/index.html', filename=None)

@app.route('/download/data')
def download_data():
    path = './static/data/data.csv'
    return send_file(path, as_attachment=True)

@app.route('/download/output-video')
def download_video():
    path = './static/assets/video/output.avi'
    return send_file(path)
