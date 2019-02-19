from google.cloud import vision
from google.cloud.vision import enums
from google.cloud.vision import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.conf['service_API_Path']

# Sending batch request to google cloud vision api for multiple pictures.
features = [
    types.Feature(type=enums.Feature.Type.TEXT_DETECTION),
    types.Feature(type=enums.Feature.Type.FACE_DETECTION),
]

requests = []
for filename in ['foo.png', 'bar.jpg', 'baz.gif']:
    with open(filename, 'rb') as image_file:
        image = types.Image(
            contents = image_file.read())
    request = types.AnnotateImageRequest(
        image=image, features=features)
    requests.append(request)

response = client.batch_annotate_images(requests)

for annotation_response in response.responses:
   do_something_with(annotation_response)