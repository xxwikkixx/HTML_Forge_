import os
import io
import time
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
from enum import Enum
from src.GoogleCloudServices import CloudServiceConfig as config
from multiprocessing import Process

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= config.conf['service_API_Path']

client = vision.ImageAnnotatorClient()

class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5

def draw_boxes(image, bounds, color):
    """Draw a border around the image using the hints in the vector list."""
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        draw.line([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y], color, width=10)
    return image


def detectPropsUri(uri, feature):
    bounds = []

    # image = vision.types.Image()
    # image.source.image_uri = uri
    with io.open(uri, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    # print(document)

    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if (feature == FeatureType.SYMBOL):
                            bounds.append(symbol.bounding_box)

                    if (feature == FeatureType.WORD):
                        bounds.append(word.bounding_box)

                if (feature == FeatureType.PARA):
                    bounds.append(paragraph.bounding_box)

            if (feature == FeatureType.BLOCK):
                bounds.append(block.bounding_box)

        if (feature == FeatureType.PAGE):
            bounds.append(block.bounding_box)
    return bounds


def render_doc_text(filein, fileout):
    image = Image.open(filein)
    bounds = detectPropsUri(filein, FeatureType.PAGE)
    draw_boxes(image, bounds, 'blue')
    bounds = detectPropsUri(filein, FeatureType.PARA)
    draw_boxes(image, bounds, 'red')
    bounds = detectPropsUri(filein, FeatureType.WORD)
    draw_boxes(image, bounds, 'yellow')

    if fileout is not 0:
        image.save(fileout)
    else:
        image.show()

# def cut_boxes(filein, fileout):



if __name__ == '__main__':

    # Scan the directory for the images
    #   create a list of them
    # The amount of files scanned is the number of files being output
    # combine the two lists together into tuples

    filesInDir = []
    numOfFiles = []

    # dirListing = os.listdir("./image")
    # for item in dirListing:
    #     if ".JPG" in item:
    #         filesInDir.append(item)

    for root, dirs, files in os.walk(os.path.abspath("./image")):
        for item in files:
            if ".JPG" in item:
                print(os.path.join(root, item))
                filesInDir.append(os.path.join(root, item))
    print(files)

    for index, things in enumerate(filesInDir):
        numOfFiles.append(str(index) + ".JPG")
    print(numOfFiles)

    funcArgs = tuple(zip(filesInDir, numOfFiles))
    print(funcArgs)

    start = time.time()
    for args in funcArgs:
        print(Process(target=render_doc_text(*args)).start())

    end = time.time()
    print(end-start)

    # for i in range(0,10):
    # render_doc_text(filein1, 'test.jpeg')
    # render_doc_text(filein2, 'test2.jpeg')
     # Average response time 7 sec
     # print("======================Request",i,"Done")



# https://googleapis.github.io/google-cloud-python/latest/vision/gapic/v1/types.html
# https://cloud.google.com/vision/docs/quickstart-client-libraries
# https://cloud.google.com/vision/docs/detecting-faces