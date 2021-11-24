import json
import os
import cv2


# Get Current Directory & Path:
path = os.getcwd()
current_path = os.listdir(path + '/img')

# Get List of Images & Annotations:
image_list = sorted(list(filter(lambda x: '.jpg' in x, current_path)))
annotation_list = sorted(list(filter(lambda x: '.json' in x, current_path)))

images = []
annotations = []

annot_pair = {
    "image": images,
    "annotation": annotations
}


for image in image_list:
    annot = os.path.splitext(image)[0] + '.json'

    if annot in annotation_list:
        annot_pair["image"] = image
        annot_pair["annotation"] = annot


for key, value in annot_pair.items():

    # Image
    if key == "image":
        _path = path + '/img/' + value
        _img = cv2.imread(_path, 0)

    # Annotation
    if key == "annotation":
        _path = path + '/img/' + value

        _read = open(_path)
        _annot = json.load(_read)
