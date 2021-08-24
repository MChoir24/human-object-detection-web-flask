from detector import Detector
import cv2


model_path = 'faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb'
odapi = Detector(path_to_ckpt=model_path)
threshold = 0.7
cap = cv2.VideoCapture('video/input/video.mp4')
# cap = cv2.VideoCapture(0)

width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

writer= cv2.VideoWriter('video/output/video.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (width,height))

n = 0
while True:
    r, img = cap.read()
    if r:
        img = cv2.resize(img, (1280, 720))

        boxes, scores, classes, num = odapi.processFrame(img)

        for i in range(len(boxes)):
            # class 1 mempresentasikan manusia
            if classes[i] == 1 and scores[i] > threshold:
                box = boxes[i]
                cv2.rectangle(img,(box[1],box[0]),(box[3],box[2]),(255,0,0),2)

        cv2.imshow("img", img)
        cv2.imwrite(f'images/{n}.jpg', img)
        n += 1

        # writer.write(img)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

cap.release()
writer.release()
cv2.destroyAllWindows()