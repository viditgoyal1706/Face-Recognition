from flask import Flask, render_template, request
import os
import cv2
from mtcnn import MTCNN
import numpy as np

app = Flask(__name__)
person_count = 0


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'single_image' in request.files:
            image = request.files['single_image']
            count, images = process_single_image(image)
            return render_template('index.html', count=count, images=images)
        elif 'bulk_images[]' in request.files:
            images = request.files.getlist('bulk_images[]')
            count, images = process_bulk_images(images)
            return render_template('index.html', count=count, images=images)
    return render_template('index.html', count=0, images=[])


def process_single_image(image):
    i=0
    image_paths=[]
    img = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_COLOR)
    count, processed_images = count_people(img , i)
    image_paths.append(processed_images)
    return count, image_paths


def process_bulk_images(images):
    total_count = 0
    image_paths = []
    for i, image in enumerate(images):
        img = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_COLOR)
        count, processed_images = count_people(img, i)
        total_count += count
        image_paths.append(processed_images)
    return total_count, image_paths


def count_people(image, i):
    image_paths = []
    detector = MTCNN()
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = detector.detect_faces(image_rgb)
    for face in results:
        if face['confidence'] > 0.6:
            x, y, width, height = face['box']
            cv2.rectangle(image, (x, y), (x+width, y+height), (0, 255, 0), 2)
    count = len(results)
    
    img_path = f"static/detected_{i}.jpg"
    cv2.imwrite(img_path, image)
    image_paths.append(img_path)
    
    return count, image_paths


if __name__ == '__main__':
    app.run(debug=True)
