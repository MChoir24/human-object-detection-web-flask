import cv2
import time

from datetime import datetime, timedelta
from math import ceil
from tools.write_csv import write_csv
from .detector import Detector

def detection_video(filename, save2):
    model_path = './tools/faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb'
    odapi = Detector(path_to_ckpt=model_path)
    threshold = 0.7
    cap = cv2.VideoCapture(filename)
    # cap = cv2.VideoCapture(0)

    width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    writer= cv2.VideoWriter(save2, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (width,height))

    pos_boxes = 0 # jumlah box positif
    pembagi = 0 # untuk merata" jumlah pos per menit
    detik = 0 # menghitung menit dari 
    detik_update = 5 # detik

    start = time.time()

    play = True
    while play:
        pembagi += 1
        r, img = cap.read()
        if r:
            img = cv2.resize(img, (1280, 720))

            boxes, scores, classes, num, elapsed_time = odapi.processFrame(img)
            for i in range(len(boxes)):
                # class 1 mempresentasikan manusia
                if classes[i] == 1 and scores[i] > threshold:
                    pos_boxes += 1 # menghitung jumlah manusia per frame
                    box = boxes[i]
                    cv2.rectangle(img,(box[1],box[0]),(box[3],box[2]),(255,0,0),2)
                    
            if int(detik % detik_update) == 0:
                hasil = ceil(pos_boxes / pembagi)
                print(hasil,'----------------------------')
                cur_datetime = str(timedelta(seconds=int(detik)))
                line = f"{cur_datetime};{hasil}"
                write_csv('./static/data/data.csv', line)

                # reset
                pos_boxes = 0
                pembagi = 0
            
            writer.write(img)
            end = time.time()
            detik = end-start
        else:
            hasil = ceil(pos_boxes / pembagi)
            print(hasil,'----------------------------')
            cur_datetime = str(timedelta(seconds=int(detik)))
            line = f"{cur_datetime};{hasil}"
            write_csv('./static/data/data.csv', line)

            play = False

    cap.release()
    writer.release()
    cv2.destroyAllWindows()