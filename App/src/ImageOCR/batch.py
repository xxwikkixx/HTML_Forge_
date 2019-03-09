import os
import time
from google.cloud import vision
from google.cloud.vision import enums
from google.cloud.vision import types
from src.GoogleCloudServices import CloudServiceConfig as config

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.conf['service_API_Path']

# client = vision.ImageAnnotatorClient()

# Sending batch request to google cloud vision api for multiple pictures.

def detect_images(client, image_paths):
    requests = []
    for image_path in image_paths:
        with open(image_path, 'rb') as image_file:
            content = image_file.read()
        image = types.Image(content=content)
        requests.append({
            'image': {
                'content': content,
            },
            'features': [{
                'type': enums.Feature.Type.DOCUMENT_TEXT_DETECTION,
            }],
        })
    response = client.batch_annotate_images(requests)
    for image_path, response in zip(image_paths, response.responses):
        yield image_path, response.full_text_annotation

if __name__ == '__main__':
    client = vision.ImageAnnotatorClient()

    filesInDir = []
    for root, dirs, files in os.walk(os.path.abspath("./image")):
        for item in files:
            if ".JPG" in item:
                print(os.path.join(root, item))
                filesInDir.append(os.path.join(root, item))


    start = time.time()
    for path, labels in detect_images(client, filesInDir):
        print(path)
        print('Labels:')
        print(labels)

    end = time.time()

    print(end-start)



# https://googleapis.github.io/google-cloud-python/latest/vision/gapic/v1/api.html