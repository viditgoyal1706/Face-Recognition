import cv2
import numpy as np
from ultralytics import YOLO
import random
import os 

my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")
my_file.close()

detection_colors = []
for i in range(len(class_list)):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    detection_colors.append((b, g, r))

model = YOLO("yolov8n.pt", "v8")

image_files = []

for file_name in os.listdir():
    if file_name.endswith("6.jpeg"):
        image_files.append(file_name)

for image_path in image_files:
    total_persons = 0
    frame = cv2.imread(image_path)
    detect_params = model.predict(source=[frame], conf=0.25, save=False)

    DP = detect_params[0].numpy()
    if len(DP) != 0:
        for i in range(len(detect_params[0])):
            boxes = detect_params[0].boxes
            box = boxes[i]
            clsID = box.cls.numpy()[0]
            conf = box.conf.numpy()[0]
            bb = box.xyxy.numpy()[0]
            
            if class_list[int(clsID)] == 'person':
                total_persons += 1
            
            cv2.rectangle(
                frame,
                (int(bb[0]), int(bb[1])),
                (int(bb[2]), int(bb[3])),
                detection_colors[int(clsID)],
                2   ,
            )
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(
                frame,
                class_list[int(clsID)] + " " + str(round(conf, 3)) + "%",
                (int(bb[0]), int(bb[1]) - 10),
                font,
                0.5,
                (255, 255, 255),
                2,
            )
    
    #print(detect_params)
    print("Number of persons detected:", total_persons)
    cv2.imshow("ObjectDetection", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

