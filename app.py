from flask import Flask, render_template, request, redirect, url_for
import requests
from PIL import Image
from io import BytesIO
from PIL import *
from PIL import ImageDraw
# Replace with your Plate Recognizer API key
API_KEY = 'a50113b95dc3e15a7fe15d726b81012db3da5840'

app = Flask(__name__)

def detect_license_plate(image):
    url = 'https://api.platerecognizer.com/v1/plate-reader/'
    headers = {'Authorization': f'Token {API_KEY}'}
    response = requests.post(url, headers=headers, files={'upload': image})
    return response.json()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image = request.files['image']
        result = detect_license_plate(image)
        if 'results' in result and len(result['results']) > 0:
            plate = result['results'][0]
            license_plate = plate['plate'].upper()
            print(type(license_plate))
            box = plate['box']
            image = Image.open(image)
            image_with_box = image.copy()
            image_with_box=image_with_box.convert('RGB')
            draw = ImageDraw.Draw(image_with_box)
            draw.rectangle([(box['xmin'], box['ymin']), (box['xmax'], box['ymax'])], outline='red', width=3)
            image_with_box.save('static/license_plate.jpg')
            return render_template('result.html', license_plate=license_plate)
        else:
            return render_template('index.html', error='No license plate detected.')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
