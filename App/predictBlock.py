# TODO(developer): Uncomment and set the following variables
from multiprocessing import Process
import os
import CloudServiceConfig as config
from google.cloud import automl_v1beta1 as automl
from google.cloud import vision
import Blocks

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.conf['service_API_Path']
project_id = config.conf['project_id']
compute_region = config.conf['compute_region']
model_id = config.conf['model_id']
thresh = config.conf["thresh"]


def detect_document(path):
    """Detects document features in an image."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
                print('Paragraph confidence: {}'.format(
                    paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    print('Word text: {} (confidence: {})'.format(
                        word_text, word.confidence))

                    for symbol in word.symbols:
                        print('\tSymbol: {} (confidence: {})'.format(
                            symbol.text, symbol.confidence))


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
    # params = {}
    # if thresh:
    params = {"score_threshold": thresh}

    response = prediction_client.predict(model_full_id, payload, params)

    prediction = []

    for result in response.payload:
        # print("Predicted class name: {}".format(result.display_name))
        # print("Predicted class score: {}".format(result.classification.score))
        temp = [result.display_name, result.classification.score]
        prediction.append(temp)
    # print("=================")
    return prediction


def imageOnReady(blocks):
    # print("Ready for AI")
    # os.chdir('..')

    for i in blocks.blocks:
        ImgPath = blocks.getBlockByID(i).getImagePath()
        Process(target=blocks.getBlockByID(i).setPrediction(predict(project_id, compute_region, model_id, ImgPath))).start()
        # getBlockByID(i).setPrediction(predict(project_id, compute_region, model_id, ImgPath))

    # for i in blocks.blocks:
    #     print("Block ", i, " ID: :", blocks.getBlockByID(i).getBlockID())
    #     print("Block ", i, " X Location: :", blocks.getBlockByID(i).getX_Location())
    #     print("Block ", i, " Y Location: :", blocks.getBlockByID(i).getY_Location())
    #     print("Block ", i, " Width: :", blocks.getBlockByID(i).get_Width())
    #     print("Block ", i, " Height: :", blocks.getBlockByID(i).get_Height())
    #     print("Block ", i, " Image Path :", blocks.getBlockByID(i).getImagePath())
    #     print("Block ", i, " Prediction: :", blocks.getBlockByID(i).getPrediction())
    #     print("Block ", i, " BEST Prediction: :", blocks.getBlockByID(i).getBestPrediction())
    #     print("Block ", i, " Second BEST Prediction: :", blocks.getBlockByID(i).getScondBest())
    #     print("========================================================================")
