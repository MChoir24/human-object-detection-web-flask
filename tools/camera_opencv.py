import os
from numpy.lib.function_base import select

from numpy.lib.histograms import _hist_bin_auto
import cv2
from .base_camera import BaseCamera
from .detector import Detector


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

        while True:
            # read current frame
            _, img = camera.read()
        
            img = cv2.resize(img, (1280, 720))

            boxes, scores, classes, num = Camera.odapi.processFrame(img)

            for i in range(len(boxes)):
                # class 1 mempresentasikan manusia
                if classes[i] == 1 and scores[i] > Camera.threshold:
                    box = boxes[i]
                    cv2.rectangle(img,(box[1],box[0]),(box[3],box[2]),(255,0,0),2)
            img = cv2.resize(img, (Camera.width, Camera.height))
            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()
