from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, flash, redirect

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENTIONS = {'jpg', 'jpeg', 'png'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENTIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        submited = request.form['deteksi']
        
        
        if submited == 'Deteksi': # jika mendeteksi citra
            # proses untuk deteksi untuk per citra
            if 'file' not in request.files:
                flash('Tidak ada citra untuk dideteksi.')
                return redirect(request.url)

            file = request.files['file']
            if file.filename == '':
                flash('Tidak ada citra untuk dideteksi.')
                return redirect(request.url)

            if file and allowed_file(file.filename):
                # save image
                # mulai deteksi img
                return render_template('home.html', datas='datas')
            else:
                flash('Terjadi kesalahan.')
                return redirect(request.url)
                
        elif submited == 'Buka Kamera': # jika mendeteksi dari kamera
            pass
            # proses untuk deteksi dari kamera
            # cam.detect_from_cam(
            #     conv_model,
            #     fc_model,
            #     last_shape_fm,
            #     pool_size,
            #     n_rois
            # )
        return render_template('home.html', )

    return render_template('home.html')


# if __name__ == '__main__':
#     app.run(debug=True)