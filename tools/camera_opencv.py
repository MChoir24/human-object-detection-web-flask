import os
import cv2
import time

from .base_camera import BaseCamera
from .detector import Detector
from .write_csv import write_csv
from math import ceil
from datetime import date, datetime


class Camera(BaseCamera):
    video_source = 0
    # video_source = 'uploads/videos/input/video.mp4'
    height = None
    width = None
    model_path = 'tools/faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb'
    odapi = Detector(path_to_ckpt=model_path)
    threshold = 0.7

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)

        Camera.width  = int(camera.get(3))   # float `width`
        Camera.height = int(camera.get(4))   # float `height`

        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        pos_boxes = 0 # jumlah box positif
        pembagi = 0 # untuk merata" jumlah pos per menit
        detik = 0 # menghitung menit dari 
        detik_update = 5 # detik

        start = time.time()
        
        while True:
            pembagi += 1
            # read current frame
            _, img = camera.read()
        
            img = cv2.resize(img, (1280, 720))

            boxes, scores, classes, num, elapsed_time = Camera.odapi.processFrame(img)

            for i in range(len(boxes)):
                # class 1 mempresentasikan manusia
                if classes[i] == 1 and scores[i] > Camera.threshold:
                    pos_boxes += 1 # menghitung jumlah manusia per frame
                    box = boxes[i]
                    cv2.rectangle(img,(box[1],box[0]),(box[3],box[2]),(255,0,0),2)
            print('detik=', detik)
            
            if detik >= detik_update:
                hasil = ceil(pos_boxes / pembagi)
                print(hasil,'----------------------------')
                cur_datetime = str(datetime.now())
                line = f"{cur_datetime};{hasil}"
                write_csv('./static/data/data_live.csv', line)

                # reset
                pos_boxes = 0
                pembagi = 0
                start = time.time()

            img = cv2.resize(img, (Camera.width, Camera.height))


            end = time.time()
            detik = end-start
            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()
