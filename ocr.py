# import the necessary packages
from collections import namedtuple
import pytesseract
import cv2

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

path = r'img1.jpg'
img = cv2.imread(path)
cv2.imshow('image', img)

img = cv2.resize(img, (280, 180))

# initialize a results list to store the document OCR parsing results
print("[INFO] OCRing document...")
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


print(parsingResults)
