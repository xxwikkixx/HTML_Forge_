"""
    This script is the first step of image processing. It takes whatever image path and import for pre-processing.
    Storing all the detected hand drawings (building blocks) into blocks database.
    Then Crop the detected blocks and pass to AI fo image classification

    Implementation steps
        0. Move Image           - to local working environment and convert any images into JPEG extension
        1. Image Cropping Unify - applying unify crop to user image to have consistent edge detection
        2. Image enhancement    - Apply gaussian and contrast to the image
        3. Thin Line Repair     - Algorithm to fix thin lines and breaking lines in the image
        4. Image Edge Detection - Contour detection
        5. Box Detection        - Detecting most outer box shape and perform crop and remove redundancy crops
        6. Add Detected Blocks  - Append all detected blocks and related information to a new singleBlock class instance
        7. Call AI              - Pass the detected and cropped images to AI for process and image classification
    ==========================================================================================
     To-do
         [Done]  Reformat and resize the image to get consistent result and image crop
         [Done]  Crop image with the x, y, w, h adjust.
         [Done]  Save the crop of the source file instead of the bolded one
         [Done]  Remove similar crops
         [Done]  Image enhancer on the original Image
         [Done]  Uses child relationship and hierarchy to know the objects within each block and eventually add it into single block attribute
         [Done]  JSON File Formatter
         [Done]  Image Drawing, boxing out detected labels
         [Done]  Full Image Path
         [Done]  Array index contour removal out of range
         [Done]  Image Dir with sessions
         [In Progress] Keeping original image size and algo rescale with it
"""

from PIL import Image, ImageEnhance, ImageDraw, ImageFont
from predictBlock import imageOnReady
from ImgProcessSession import ImageProcessSession
from Blocks import Blocks
from imutils.contours import sort_contours
from PIL import Image
import cv2
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import time

# Set true if debugging
Image_Debug = False
Console_Logger = False

# This is just for the py plotting results (debug purposes)
fig = plt.figure(figsize=(8, 8))
columns = 3
rows = 3

# Unify crop and re-rescaling
IMAGE_HEIGHT = 1000
IMAGE_WIDTH = 1500

# For line bolding
ITERATIONS = 0
TARESHOLD = 20
MIN_LINE_LENG = 30
MAX_LINE_GAP = 25

# List to store detected block contours [x,y,w,h]
exported_contours = []

# Current script work environment
FULL_PATH_TO_THIS_FOLDER = (os.getcwd())


def image_Rescale(image_Path):
    """
        This will rescale all in user image into 3:2 Image ratio
        Perform and save to the same image path

        :param image_Path: string : Path to image
    """
    size = IMAGE_HEIGHT, IMAGE_WIDTH
    im = Image.open(image_Path)
    im.thumbnail(size)
    newimg = im.resize(size)
    newimg.save(image_Path)


def applyGaussian(image_Path):
    """
        Apply Gaussian Image enhancement and contrasting
        Perform and save to the same image path
        :param image_Path: string : Path to image
    """

    # read the image
    img = cv2.imread(image_Path)
    # convert image to gray scale imag
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # apply gaussian and threshold
    T = threshold_local(gray, 21, offset=80, method="gaussian")
    gray = (gray > T).astype("uint8") * 255
    # save image to the same image path
    cv2.imwrite(image_Path, gray)


def fileConvert(imgPath, savePath):
    """
        Takes in an image path, and save to a new destination and converts to monochrome
        Perform and save to the same image path
        :param imgPath: Import image path
        :param savePath: Export image path
    """
    im = Image.open(imgPath)
    # bg = Image.new("RGB", crop_img.size, (255, 255, 255))
    # rgb_im = im.convert('RGB')

    # Convert to monochrome
    im = im.convert('1')
    im.save(savePath)


def cornerFit(imgPath):
    """
        cornerFit detects the most outer corners and perform and tight crop around it.
        This will ensure better and more unified blx detection
        Perform and save to the same image path
    :param imgPath: path to the image
    """

    # applyGaussian(imgPath)

    # read the image
    img = cv2.imread(imgPath)
    # convert image to gray scale image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # detect corners with the goodFeaturesToTrack function.
    corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
    corners = np.int0(corners)

    # we iterate through each corner,
    # making a circle at each point that we think is a corner.
    x_arr, y_arr = [], []

    for i in corners:
        x, y = i.ravel()
        x_arr.append(x)
        y_arr.append(y)

        # Draw circle if for debugging
        # cv2.circle(img, (x, y), 20, 255, -1)

    # Find the most outer edges
    X_MIN, X_MAX = min(x_arr), max(x_arr)
    Y_MIN, Y_MAX = min(y_arr), max(y_arr)

    # cropping data [x0:x1:y0:y1]
    crop_img = img[Y_MIN - 100: Y_MAX + 100, X_MIN - 100: X_MAX + 100]

    # plt.imshow(img), plt.show()
    # plt.imshow(crop_img), plt.show()

    # Save Crop
    cv2.imwrite(imgPath, crop_img)


# Not being used
def enhanceImage(path):
    im = Image.open(path)
    # enhancer = ImageEnhance.Brightness(im)
    temp = ImageEnhance.Sharpness(im)
    enhanced_im = temp.enhance(10.0)
    enhanced_im.save(path)


def line_Bolding(imgpath):
    """
        line_Balding function takes an image path and draw lines to places where if the user drawings' line are too thin
        :param imgpath: string Path to the image
    """

    img = cv2.imread(imgpath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Canny function to enhance edges
    edges = cv2.Canny(gray, 255, 255, apertureSize=3)
    if Image_Debug: cv2.imwrite(newSession.getDebugDir() + 'cann.jpg', edges)

    # HoughLinesP()
    # pass in params (image*, rho, theta, threshold[, lines[, minLineLength[, maxLineGap]]])
    # threshold: should not be adjusted co-relate to the Canny Function
    # minLineLength: Threshold how the shortest line
    # maxLineGap: Gap length that are allowed  between line to line inorder to consider it as a line
    lines = cv2.HoughLinesP(edges, rho=1, theta=1 * np.pi / 180, threshold=TARESHOLD, minLineLength=MIN_LINE_LENG,
                            maxLineGap=MAX_LINE_GAP)

    # Iterate through the detected thin lines and draw with thicker lines
    for i in range(0, len(lines)):
        x1, y1, x2, y2 = lines[i][0]
        # Draw the thicker black line on to the image
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 0), 2)

    cv2.imwrite(newSession.getDebugDir() + 'houghlines.jpg', img)  # For debug use
    # cv2.imwrite(imgpath, img)
    cv2.destroyAllWindows()


def box_extraction(original_image_path, img_for_box_extraction_path, cropped_dir_path, blocks):
    """
        Function for Hand drawn Box Detection
        Detects Blocks, remove similar crops, apply crops, and store detected blocks

    :param original_image_path: string              Original Image
    :param img_for_box_extraction_path: string      Image with all the enhancements
    :param cropped_dir_path: string                 The detected and crops' output folder
    :param blocks: Object                           Block class instance to store all the detected information
    :return:
    """

    # Read the original image
    orginal_image = cv2.imread(original_image_path, 0)
    # Read the enhanced image
    img = cv2.imread(img_for_box_extraction_path, 0)
    # Threshold and contrast the image
    (thresh, img_bin) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Invert Image for better contrast and detection
    try:
        img_bin = 255 - img_bin  # Invert the image
    except:
        print("failed to invert")

    if Image_Debug: cv2.imwrite(newSession.getDebugDir() + "Image_bin.jpg", img_bin)

    # Defining a kernel length
    kernel_length = np.array(img).shape[1] // 80
    # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
    # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    # A kernel of (3 X 3) ones.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # Morphological operation to detect verticle lines from an image

    # Morphological operation to detect vertical lines from an image
    img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=ITERATIONS)
    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=ITERATIONS)
    if Image_Debug: cv2.imwrite(newSession.getDebugDir() + "verticle_lines.jpg", verticle_lines_img)
    # Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=ITERATIONS)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=ITERATIONS)
    if Image_Debug: cv2.imwrite(newSession.getDebugDir() + "horizontal_lines.jpg", horizontal_lines_img)

    # summation or two images
    alpha = 0.5
    beta = 1.0 - alpha
    img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=ITERATIONS)
    (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    if Image_Debug: cv2.imwrite(newSession.getDebugDir() + "img_final_bin.jpg", img_final_bin)

    # Find contours for image, which will detect all the boxes
    contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_LIST, cv2.CHAIN_APPRO)
    # Sort all the contours by top to bottom.
    (contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")
    # (contours, boundingBoxes) = sort_contours(contours, method="bottom-to-top")

    if Console_Logger: print("============ Hierarchy ================")
    if Console_Logger: print(hierarchy)
    if Console_Logger: print("=======================================")

    # Find the suitable crops
    for c in contours:
        # Returns the location and width,height for every contour
        x, y, w, h = cv2.boundingRect(c)
        # if Console_Logger: print("width: ", w, "\theight:", h)
        # if Console_Logger: print("========================")
        # If the box height is greater then 700 or width is >700, then only save it as a box in "cropped/" folder.
        # if ((w > 500 and h > 20) or (h > 500 and w > 20)) and w != 3000 and h != 2000 and x > 50 and y > 50:
        if ((w > IMAGE_WIDTH * 0.25 and h > IMAGE_HEIGHT * 0.1) or (
                h > 400 and w > 50)) and w != IMAGE_HEIGHT and h != IMAGE_WIDTH and x > 10 and y > 10:
            if Console_Logger: print("Crop Log: ", [x, y, w, h])
            # Add all the suitable crops to a list
            exported_contours.append([x, y, w, h])

    # for i in range(0, len(exported_contours)):
    #     for j in range(0, len(exported_contours)):
    #         print (i, j)
    #         # Compare X axis and Y see if it is similar crop
    #         if 0 < i < len(exported_contours) and 0 < j < len(exported_contours):
    #             if exported_contours[i] != exported_contours[j]:
    #                 print("IN Condition")
    #                 temp_1, temp_2 = float(abs(sum(exported_contours[i]))), float(abs(sum(exported_contours[j])))
    #                 # if two images are similar within the range
    #                 print("lalala",temp_2/temp_1)
    #                 if 0.95 < temp_1 / temp_2 < 1.05:
    #                     if Console_Logger: print("Delete Log: Image Similar contour removed")
    #
    #                     # Choose the bigger contour and pop the smaller crop
    #                     if ((exported_contours[j][2] + exported_contours[j][3]) > exported_contours[i][2] +
    #                             exported_contours[i][3]):
    #                         if Console_Logger: print("  |----->", exported_contours[i])
    #                         new_img = orginal_image[
    #                                   exported_contours[j][1]:exported_contours[j][1] + exported_contours[j][3],
    #                                   exported_contours[j][0]:exported_contours[j][0] + exported_contours[j][2]]
    #                         cv2.imwrite(cropped_dir_path + "Deleted_" + str(j) + '.png', new_img)
    #                         exported_contours.pop(j)
    #                         j -= 1  # re-compare previous j element index since it is removed
    #                     else:
    #                         if Console_Logger: print("  |----->", exported_contours[i])
    #                         new_img = orginal_image[
    #                                   exported_contours[i][1]:exported_contours[i][1] + exported_contours[i][3],
    #                                   exported_contours[i][0]:exported_contours[i][0] + exported_contours[i][2]]
    #                         cv2.imwrite(cropped_dir_path + "Deleted_" + str(i) + '.png', new_img)
    #                         exported_contours.pop(i)
    #                         i -= 1  # re-compare previous i element index since it is removed
    #
    # else:
    #     raise IndexError("Array pop index exception!!")


    # Iterate through final candidates and remove repetitive blocks
    for i in range(len(exported_contours) - 1, 0, -1):
        for j in range(i):
            # Compare X axis and Y see if it is similar crop
            if i <= len(exported_contours) and j <= len(exported_contours):
                temp_1, temp_2 = float(abs(sum(exported_contours[i]))), float(abs(sum(exported_contours[j])))
                # if two images are 98% similar within the range
                if 0.98 < (temp_1 / temp_2) < 1.05:
                    if Console_Logger: print("Delete Log: Image Similar contour removed")
                    # Choose the bigger contour and pop the smaller crop
                    if ((exported_contours[j][2] + exported_contours[j][3]) > exported_contours[i][2] +
                            exported_contours[i][3]):
                        if Console_Logger: print("  |----->", exported_contours[i])
                        new_img = orginal_image[
                                  exported_contours[j][1]:exported_contours[j][1] + exported_contours[j][3],
                                  exported_contours[j][0]:exported_contours[j][0] + exported_contours[j][2]]
                        cv2.imwrite(cropped_dir_path + "Deleted_" + str(j) + '.png', new_img)
                        # remove the contour
                        exported_contours.pop(j)
                        # re-compare previous j element index since it is removed
                        j -= 1
                    else:
                        if Console_Logger: print("  |----->", exported_contours[i])
                        new_img = orginal_image[
                                  exported_contours[i][1]:exported_contours[i][1] + exported_contours[i][3],
                                  exported_contours[i][0]:exported_contours[i][0] + exported_contours[i][2]]
                        cv2.imwrite(cropped_dir_path + "Deleted_" + str(i) + '.png', new_img)
                        # remove the contour
                        exported_contours.pop(i)
                        # re-compare previous i element index since it is removed
                        i -= 1
            else:
                raise IndexError("Array pop index exception!!")


    if Console_Logger: print("============================")

    # Start cropping image and create single block instances
    if Console_Logger: print("Final Exported Contours: ", exported_contours)
    idx = 0
    for i in range(0, len(exported_contours)):
        idx += 1
        x, y, w, h = exported_contours[i]

        # The crop is right is too tight, since it is right on the border, this adjusts with bigger border
        x -= 30
        y -= 30
        w += 50
        h += 50

        # Cropping the original image
        new_img = orginal_image[y:y + h, x:x + w]

        # Save to assigned path
        cv2.imwrite(cropped_dir_path + str(idx) + '.png', new_img)

        # Create a Single Block Instance and add Single Block to Blocks Database
        createSingleBlockInstance(blocks, idx, x, y, h, w, cropped_dir_path + str(idx) + '.png')

        # Display cropped image onto the mlplot
        if Image_Debug: fig.add_subplot(rows, columns, idx)
        if Image_Debug: plt.imshow(new_img)

    if Image_Debug: plt.show()
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def createSingleBlockInstance(blocks, id, x, y, h, w, sorcePath):
    """
        create all the detected blocks as single instance
        :param blocks: Object Block Class instance
        :param id: int The id that is assigning to the block
        :param x: int  X Axis of the detected block
        :param y: int  Y Axis of the detected block
        :param h: int  Height of the detected block
        :param w: int  Width of the detected block
        :param sorcePath: String  The path where the image is saved at
    """
    blocks.addBlock()
    blocks.getBlockByID(id).setX_Location(x)
    blocks.getBlockByID(id).setY_Location(y)
    blocks.getBlockByID(id).set_Height(h)
    blocks.getBlockByID(id).set_Width(w)
    blocks.getBlockByID(id).setImagePath(sorcePath)


# ==================== Helper Function and Tools ========================
def clearImageDir(folder_path):
    """
     !!!!!! Be mindful all the files under that dir will be deleted
     clean output image dir for new session

    :param folder_path: String  Path to the Dir you want to remove all the file
    """
    files = glob.glob(folder_path + "*")
    for f in files:
        os.remove(f)



def execute_Box_Detection(path, blocks):
    """
    Helper Function of steps processing the box detection

    :param path: String Path the image for processing
    :param blocks: Object  Object Block Class instance to store detected boxes
    :return:
    """
    # Delete images from previous session
    # clearImageDir(imageOutputFileDirectory)

    # rescale image size to have more unified image to work with
    image_Rescale(path)

    # Analyze thin lines and enhance it
    line_Bolding(path)

    # Execute the block detection feature

    # @params:[original image path, enhancedImagePath, exportImageDir]
    cp_Dir = newSession.getCropDir()
    box_extraction(path, newSession.getDebugDir() + 'houghlines.jpg', cp_Dir, blocks)


# Once the AI is finished, draw the detected boxes on to the original image
def labelDrawBox(blocks, src):
    source_img = Image.open(src).convert("RGB")
    draw = ImageDraw.Draw(source_img)
    # font = ImageFont.load_default().font
    font = ImageFont.truetype(FULL_PATH_TO_THIS_FOLDER + "/arial.ttf", 28)
    for i in blocks.blocks:
        x = blocks.getBlockByID(i).getX_Location()
        y = blocks.getBlockByID(i).getY_Location()
        w = blocks.getBlockByID(i).get_Width()
        h = blocks.getBlockByID(i).get_Height()

        draw.rectangle(((x, y), (x + w, y + h)), outline="red", width=4)
        draw.text((x + 10, y), str(blocks.getBlockByID(i).getBestPrediction()), fill="red", font=font)
    source_img.show()
    source_img.save(src, "JPEG")


def startSession(path_to_image):
    # Create and initialize new Session
    global newSession
    newSession = ImageProcessSession()
    newSession.userImageImport(path_to_image)

    # Initialize a new session base on user's request
    imgName = newSession.getSessionID() + ".jpg"
    fileConvert(newSession.getpathToUserImage(), newSession.getSessionPath() + "/" + imgName)

    # Image first got fed through corner detection for initial crop [This will get more unify result]
    cornerFit(newSession.getSessionPath() + "/" + imgName)

    blocksDB = Blocks()
    # Pass in the pre cropped image for building block detection
    execute_Box_Detection(newSession.getSessionPath() + "/" + imgName, blocksDB)

    # All building block infos stored in blocks class
    # Call AI for further process
    imageOnReady(blocksDB)

    labelDrawBox(blocksDB, newSession.getSessionPath() + imgName)
    blocksDB.JSONFormat(newSession.getSessionPath() + "/" + "data.json")

    # for i in blocksDB.blocks:
    #     print("Block ", i, " ID: :", blocksDB.getBlockByID(i).getBlockID())
    #     print("Block ", i, " X Location: :", blocksDB.getBlockByID(i).getX_Location())
    #     print("Block ", i, " Y Location: :", blocksDB.getBlockByID(i).getY_Location())
    #     print("Block ", i, " Width: :", blocksDB.getBlockByID(i).get_Width())
    #     print("Block ", i, " Height: :", blocksDB.getBlockByID(i).get_Height())
    #     print("Block ", i, " Image Path :", blocksDB.getBlockByID(i).getImagePath())
    #
    #     # getBlockByID(i).setPrediction(predict(project_id, compute_region, model_id, ImgPath))
    #     print("Block ", i, " Prediction: :", blocksDB.getBlockByID(i).getPrediction())
    #     print("Block ", i, " BEST Prediction: :", blocksDB.getBlockByID(i).getBestPrediction())
    #     print("Block ", i, " Second BEST Prediction: :", blocksDB.getBlockByID(i).getScondBest())
    #     print("========================================================================")

    return newSession.getSessionID(), newSession.getSessionPath() + "data.json"


# Main
if __name__ == "__main__":
    # Initialize timer for run time speed
    start = time.time()
    # clearImageDir("/Users/edwardlai/Documents/2019 Spring Assignments/HTML_Forge/App/src/ImageProcessing/UserUpload/")

    # passToken(newsession.getSessionID())
    # startSession(
    #     "/Users/edwardlai/Documents/2019 Spring Assignments/HTML_Forge/App/Sample Images/Sample_1.jpg")

    end = time.time()
    print("Process Run Time: Seconds: ", end - start)