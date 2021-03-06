#!/usr/bin/env python
from importlib import import_module
from flask import Flask, render_template, Response, send_file
from PIL import Image
from flask.helpers import url_for
from tools.detector import Detector

import io
import os
import numpy as np


# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from tools.camera_opencv import Camera


app = Flask(__name__)
import upload #upload routes

@app.route('/live-video')
def index():
    """Video streaming home page."""
    return render_template('pages/live_video.html')


def gen(camera):
    """Video streaming generator function."""
    
    while True:
        cam = camera
        frame = cam.get_frame()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/download/data-live')
def download():
    path = './static/data/data_live.csv'
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)
