# TODO(developer): Uncomment and set the following variables
import asyncio
import os
from pathlib import Path

from GoogleCloudServices import CloudServiceConfig as config
from google.cloud import automl_v1beta1 as automl
from google.cloud import vision
from multiprocessing import Pool

from Blocks.Blocks import blocks, getBlockByID

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.conf['service_API_Path']

project_id = config.conf['project_id']
compute_region = config.conf['compute_region']
model_id = config.conf['model_id']
# file_path = "/Users/edwardlai/Downloads/IMG_1532.JPG"



def detect_crop_hints(path):
    """Detects crop hints in an image."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    crop_hints_params = vision.types.CropHintsParams(aspect_ratios=[1.77])
    image_context = vision.types.ImageContext(
        crop_hints_params=crop_hints_params)

    response = client.crop_hints(image=image, image_context=image_context)
    hints = response.crop_hints_annotation.crop_hints

    for n, hint in enumerate(hints):
        print('\nCrop Hint: {}'.format(n))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                     for vertex in hint.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))


def localize_objects(path):
    """Localize objects in the local image.
    Args:
    path: The path to the local file.
    """
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))


def predict(project_id, compute_region, model_id, file_path):
    multilabel = True  # for multilabel or False for multiclass
    score_threshold = "0.5"
    client = vision.ImageAnnotatorClient()
    automl_client = automl.AutoMlClient()

    # Get the full path of the model.
    model_full_id = automl_client.model_path(
        project_id, compute_region, model_id
    )

    # Create client for prediction service.
    prediction_client = automl.PredictionServiceClient()

    # Read the image and assign to payload.
    with open(file_path, "rb") as image_file:
        content = image_file.read()
    payload = {"image": {"image_bytes": content}}
    image = vision.types.Image(content=content)

    # params is additional domain-specific parameters.
    # score_threshold is used to filter the result
    # Initialize params
    params = {}
    if score_threshold:
        params = {"score_threshold": score_threshold}

    objects = client.object_localization(
        image=image).localized_object_annotations

    response = prediction_client.predict(model_full_id, payload, params)
    print("Prediction results:")
    for result in response.payload:
        print("Predicted class name: {}".format(result.display_name))
        print("Predicted class score: {}".format(result.classification.score))





def imageOnReady():

    print("Ready for AI")
    os.chdir('..')
    file_path = "ImageProcessing/cropped/2.png"

    predict(project_id, compute_region, model_id, file_path)
    for i in blocks:
        print("Block ", i, " ID: :", getBlockByID(i).getBlockID())
        print("Block ", i, " X Location: :", getBlockByID(i).getX_Location())
        print("Block ", i, " Y Location: :", getBlockByID(i).getY_Location())
        print("Block ", i, " Width: :", getBlockByID(i).get_Width())
        print("Block ", i, " Height: :", getBlockByID(i).get_Height())
        print("Block ", i, " image path: :", getBlockByID(i).getImagePath())
        print("========================================================================")
