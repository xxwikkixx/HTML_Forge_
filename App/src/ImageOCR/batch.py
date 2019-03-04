import os
from google.cloud import vision
from google.cloud.vision import enums
from google.cloud.vision import types
from src.GoogleCloudServices import CloudServiceConfig as config

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.conf['service_API_Path']

# client = vision.ImageAnnotatorClient()

# Sending batch request to google cloud vision api for multiple pictures.
features = [
    types.Feature(type=enums.Feature.Type.DOCUMENT_TEXT_DETECTION),
]


# requests = []
# for filename in files:
#     with open(filename, 'rb') as image_file:
#         image = types.Image(
#             contents = image_file.read())
#     request = types.AnnotateImageRequest(
#         image=image, features=features)
#     requests.append(request)
#
# response = client.batch_annotate_images(requests)
#
# for annotation_response in response.responses:
#    print(annotation_response)

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
                'type': enums.Feature.Type.LABEL_DETECTION,
            }],
        })
    response = client.batch_annotate_images(requests)
    for image_path, response in zip(image_paths, response.responses):
        yield image_path, response.full_text_annotation

if __name__ == '__main__':
    client = vision.ImageAnnotatorClient()

    files = []
    dirListing = os.listdir("./image")
    for item in dirListing:
        if ".JPG" in item:
            files.append(item)
    print(files)

    for path, labels, web in detect_images(client, files):
        print(path)
        print('Labels:')
        print(labels)
        print('Web')
        print(web)
