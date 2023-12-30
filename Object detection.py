'''import cv2
from matplotlib import pyplot as plt
from mtcnn import MTCNN
#from sklearn.metrics import confusion_matrix
import seaborn as sns
from pathlib import Path
import os

png_files = []

for file_name in os.listdir():
    if file_name.endswith(".jpeg"):
        png_files.append(file_name)

for image_path in png_files:

    image = cv2.imread(image_path)

    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    detector = MTCNN()

    faces = detector.detect_faces(image_rgb)

    person_count = 0
    for face in faces:
        if face['confidence'] > 0.2:
            person_count += 1
            x, y, width, height = face['box']
            cv2.rectangle(image, (x, y), (x+width, y+height), (0, 255, 0), 2)

    print("Number of persons:", person_count)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()/'''

import cv2
from matplotlib import pyplot as plt
from mtcnn import MTCNN
#from sklearn.metrics import confusion_matrix
import seaborn as sns
from pathlib import Path
import os

png_files = []

for file_name in os.listdir():
    if file_name.endswith("19.jpeg"):
        png_files.append(file_name)

for image_path in png_files:

    image = cv2.imread(image_path)

    scale_percent = 150
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    image = cv2.resize(image, (width, height))

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    detector = MTCNN()

    faces = detector.detect_faces(image_rgb)

    person_count = 0
    for face in faces:
        if face['confidence'] > 0.7:
            person_count += 1
            x, y, width, height = face['box']
            cv2.rectangle(image, (x, y), (x+width, y+height), (0, 255, 0), 2)

    print("Number of persons:", person_count)
    print("image path:",image_path)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()
