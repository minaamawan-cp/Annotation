import os
import cv2
import json
import pytesseract

# Get Current Directory & Path:
path_parent = os.path.dirname(os.getcwd())
_path = os.listdir(path_parent + '/images')

# Get List of Images & Annotations:
image_list = sorted(list(filter(lambda x: '.jpg' in x, _path)))
annotation_list = sorted(list(filter(lambda x: '.json' in x, _path)))

images = []
annotations = []


def process():
    # Start Process:
    for image in image_list:
        annot = os.path.splitext(image)[0] + '.json'

        if annot in annotation_list:
            annotations_pair(image, annot)

    # # Text Recognition:
    # _path = path_parent + '/temp/'
    # print(_path)
    #
    #     cropped_img = cv2.imread(file
    # gray = get_grayscale(cropped_img)
    # cv2.imshow('img', gray)

    # custom_config = r'--oem 3 --psm 6'
    # pytesseract.image_to_string(img, config=custom_config)


def annotations_pair(image, annotation):
    # Initialize:
    id = ''
    label = ''
    x = ''
    y = ''
    w = ''
    h = ''

    # Temporary Path:
    _path = path_parent + '/images/'

    # Read Image:
    _img = cv2.imread(f'{_path}' + f'{image}')

    # Read JSON:
    _read = open(f'{_path}' + f'{annotation}')
    _annot = json.load(_read)

    # Parse Values
    for item in _annot["Annotations"]:

        if item["id"]:
            id = item["id"]

        if item["label"]:
            label = item["label"]

        if item["bbox"]:
            x = item["bbox"][0]
            y = item["bbox"][1]
            w = item["bbox"][2]
            h = item["bbox"][3]

        # Draw Rectangle:
        # cv2.rectangle(_img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Crop Images & Save:
        temp_directory = path_parent + '/temp/'
        os.chdir(temp_directory)

        # Save Cropped File
        baseImageName = os.path.splitext(image)[0]
        baseBox = f'{baseImageName}_{id}_{label}' + '.jpg'
        _cropped = _img[y: y + h, x: x + w].copy()
        cv2.imwrite(baseBox, _cropped)


# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 5)


# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


process()
