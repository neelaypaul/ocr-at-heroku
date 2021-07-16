# import the necessary packages
from collections import namedtuple
import pytesseract
import cv2
import pyrebase
from flask import Flask, render_template, request, jsonify


firebaseconfig = {
    'apiKey': "AIzaSyB4X8htz2B2n2Oa3WC6HHA5KmpSUWVP0LE",
    'authDomain': "ocr-heroku.firebaseapp.com",
    'projectId': "ocr-heroku",
    'storageBucket': "ocr-heroku.appspot.com",
    'messagingSenderId': "929906221321",
    'appId': "1:929906221321:web:82d99c84ed1c35bbe1f3d8",
    'measurementId': "G-XZBYLB1RHZ",
    'databaseURL':''
}

firebase = pyrebase.initialize_app(firebaseconfig)
storage= firebase.storage()

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'

# create a named tuple which we can use to create locations of the
# input document which we wish to OCR
OCRLocation = namedtuple("OCRLocation", ["id", "bbox", "filter_keywords"])

# define the locations of each area of the document we wish to OCR
OCR_LOCATIONS = [
    OCRLocation("Name", (44, 34, 80, 35),
                ["middle", "initial", "first", "name"]),
    OCRLocation("Gender", (94, 83, 20, 20),
                ["last", "name"]),
    OCRLocation("DOB", (90, 110, 70, 20),
                ["address"]),
    OCRLocation("Place_of_birth", (181, 112, 37, 13),
                ["city", "zip", "town", "state"])
]

app = Flask(__name__)

@app.route('/')
def upload_file():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file1():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)

        path = f.filename
        img = cv2.imread(path)
        img = cv2.resize(img, (280, 180))

        parsingResults = {}

        # loop over the locations of the document we are going to OCR
        for loc in OCR_LOCATIONS:
            # extract the OCR ROI from the aligned image
            id = loc.id

            (x, y, w, h) = loc.bbox
            roi = img[y:y + h, x:x + w]
            # OCR the ROI using Tesseracts
            rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
            text = pytesseract.image_to_string(rgb)
            text = text.replace('\n', ' ')
            text = list(s for s in text if s.isprintable())
            text = ''.join(text)
            text = text.strip()
            parsingResults[id] = text
        j = jsonify(parsingResults)

        return j

@app.route('/uploader_fb', methods=['GET', 'POST'])
def upload_file2():
    if request.method == 'GET':
        storage.child("img1.jpg").download("", "img1.jpg")

        path = r"img1.jpg"
        img = cv2.imread(path)
        img = cv2.resize(img, (280, 180))

        parsingResults = {}

        # loop over the locations of the document we are going to OCR
        for loc in OCR_LOCATIONS:
            # extract the OCR ROI from the aligned image
            id = loc.id

            (x, y, w, h) = loc.bbox
            roi = img[y:y + h, x:x + w]
            # OCR the ROI using Tesseracts
            rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
            text = pytesseract.image_to_string(rgb)
            text = text.replace('\n', ' ')
            text = list(s for s in text if s.isprintable())
            text = ''.join(text)
            text = text.strip()
            parsingResults[id] = text
        j = jsonify(parsingResults)

        return j

if __name__ == '__main__':
    app.run(debug=True)