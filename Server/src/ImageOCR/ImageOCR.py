import os
import io
from google.cloud import vision
from google.cloud.vision import types
import json

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/wikki/Downloads/clientTempAPIKey_htmlforge-d8f980d8c5e9.json"

client = vision.ImageAnnotatorClient()

path = '/uploadBlocks/'

# Detect from local data
def detect_props(path):
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content = content)
    response = client.image_properties(image=image)
    props = response.image_properties_annotation

# Detect from online URL of the image
def detectPropsUri(uri):
    image = vision.types.Image()
    image.source.image_uri = uri
    response = client.text_detection(image=image)
    labels = response.text_annotations
    print(labels)

detectPropsUri('http://digitalnativestudios.com/textmeshpro/docs/rich-text/colors.png')

# https://googleapis.github.io/google-cloud-python/latest/vision/gapic/v1/types.html
# https://cloud.google.com/vision/docs/quickstart-client-libraries
# https://cloud.google.com/vision/docs/detecting-faces