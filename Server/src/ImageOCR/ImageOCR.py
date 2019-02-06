import os
import io
from google.cloud import vision
from google.cloud.vision import types

client = vision.ImageAnnotatorClient()

path = '/uploadBlocks/'

def detect_props(path):
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content = content)

    response = client.image_properties(image=image)

    props = response.image_properties_annotation

    