from PIL import Image, ImageEnhance, ImageDraw, ImageFont
from predictBlock import imageOnReady
from ImgProcessSession import ImageProcessSession
from Blocks import Blocks
from imutils.contours import sort_contours
import cv2
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import time


Image_Debug = False
Console_Logger = False

# This is just for the py plotting results (debug purposes)
fig = plt.figure(figsize=(8, 8))
columns = 3
rows = 3

IMAGE_HEIGHT = 1000
IMAGE_WIDTH = 1500
ITERATIONS = 0
TARESHOLD = 20
MIN_LINE_LENG = 30
MAX_LINE_GAP = 25
exported_contours = []
FULL_PATH_TO_THIS_FOLDER = (os.getcwd())

print ("Full", FULL_PATH_TO_THIS_FOLDER)


# 1
#  This will rescale all in user image into 3:2 Image ratio
def image_Rescale(image_Path):
    size = IMAGE_HEIGHT, IMAGE_WIDTH
    from PIL import Image
    im = Image.open(image_Path)
    im.thumbnail(size)
    newimg = im.resize(size)
    newimg.save(image_Path)


def applyGaussian(path):
    # read the image
    img = cv2.imread(path)
    # convert image to gray scale imag
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    T = threshold_local(gray, 21, offset=80, method="gaussian")
    gray = (gray > T).astype("uint8") * 255
    cv2.imwrite(path, gray)


def fileConvert(imgPath, savePath):
    im = Image.open(imgPath)
    # bg = Image.new("RGB", crop_img.size, (255, 255, 255))
    rgb_im = im.convert('RGB')
    rgb_im = rgb_im.convert('1')
    rgb_im.save(savePath)


def cornerFit(imgPath):
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
    # print("corners:", corners)
    x_arr = []
    y_arr = []
    for i in corners:
        x, y = i.ravel()
        x_arr.append(x)
        y_arr.append(y)
        # cv2.circle(img, (x, y), 20, 255, -1)

    X_MIN, X_MAX = min(x_arr), max(x_arr)
    Y_MIN, Y_MAX = min(y_arr), max(y_arr)

    # print(X_MIN, X_MAX, Y_MIN, Y_MAX)

    crop_img = img[Y_MIN - 100: Y_MAX + 100, X_MIN - 100: X_MAX + 100]

    # plt.imshow(img), plt.show()
    # plt.imshow(crop_img), plt.show()
    cv2.imwrite(imgPath, crop_img)


# Not being used
def enhanceImage(path):
    im = Image.open(path)
    # enhancer = ImageEnhance.Brightness(im)
    temp = ImageEnhance.Sharpness(im)
    enhanced_im = temp.enhance(10.0)
    enhanced_im.save(path)


# 2
# line_Balding function
# Param: a openCV Bin Image
# Return: Bolded openCV Bin Image
def line_Bolding(imgpath):
    img = cv2.imread(imgpath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 255, 255, apertureSize=3)
    if Image_Debug: cv2.imwrite(newSession.getDebugDir() + 'cann.jpg', edges)

    # HoughLinesP()
    # pass in params (image*, rho, theta, threshold[, lines[, minLineLength[, maxLineGap]]])
    # threshold: should not be adjusted co-relate to the Canny Function
    # minLineLength: Threshold how the shortest line
    # maxLineGap: Gap length that are allowed  between line to line inorder to consider it as a line
    lines = cv2.HoughLinesP(edges, rho=1, theta=1 * np.pi / 180, threshold=TARESHOLD, minLineLength=MIN_LINE_LENG,
                            maxLineGap=MAX_LINE_GAP)

    for i in range(0, len(lines)):
        x1, y1, x2, y2 = lines[i][0]
        # Draw the thicker black line on to the image
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 0), 2)

    cv2.imwrite(newSession.getDebugDir() + 'houghlines.jpg', img)  # For debug use
    # cv2.imwrite(imgpath, img)
    cv2.destroyAllWindows()


# 3
# Function for box detection
def box_extraction(original_image_path, img_for_box_extraction_path, cropped_dir_path, blocks):
    orginal_image = cv2.imread(original_image_path, 0)

    img = cv2.imread(img_for_box_extraction_path, 0)  # Read the image
    (thresh, img_bin) = cv2.threshold(img, 128, 255,
                                      cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Threshold and contrast the image

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
            exported_contours.append([x, y, w, h])

    print(exported_contours)

    # for i in range(0, len(exported_contours)):
    #     for j in range(0, len(exported_contours)):
    #         print (i, j)
    #         # Compare X axis and Y see if it is similar crop
    #         if 0 < i < len(exported_contours) and 0 < j < len(exported_contours):
    #             if exported_contours[i] != exported_contours[j]:
    #                 print("IN Condition")
    #                 temp_1, temp_2 = abs(sum(exported_contours[i])), abs(sum(exported_contours[j]))
    #                 # if two images are similar within the range
    #                 if 0.98 < (temp_1 / temp_2) < 1.02:
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
            # else:
            #     raise IndexError("Array pop index exception!!")

    # Iterate through final candidates and remove repetitive blocks
    # for i in range(len(exported_contours) - 1, 0, -1):
    #     for j in range(i):

    if Console_Logger: print("============================")

    # Start cropping image and create single block instances
    if Console_Logger: print("Final Exported Contours: ", exported_contours)

    idx = 0
    for i in range(0, len(exported_contours)):
        idx += 1
        x, y, w, h = exported_contours[i]

        # The crop is right is too tight since it is right on the border, this adjusts with bigger border
        x -= 30
        y -= 30
        w += 50
        h += 50

        # Cropping the original image
        new_img = orginal_image[y:y + h, x:x + w]

        cv2.imwrite(cropped_dir_path + str(idx) + '.png', new_img)
        createSingleBlockInstance(blocks, idx, x, y, h, w,
                                   cropped_dir_path + str(idx) + '.png')

        # Display cropped image onto the mlplot
        if Image_Debug: fig.add_subplot(rows, columns, idx)
        if Image_Debug: plt.imshow(new_img)

    if Image_Debug: plt.show()
    # if Image_Debug: cv2.imshow('boxed', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 3.5
# create all the detected blocks as single instance
def createSingleBlockInstance(blocks, id, x, y, h, w, sorcePath):
    blocks.addBlock()
    blocks.getBlockByID(id).setX_Location(x)
    blocks.getBlockByID(id).setY_Location(y)
    blocks.getBlockByID(id).set_Height(h)
    blocks.getBlockByID(id).set_Width(w)
    blocks.getBlockByID(id).setImagePath(sorcePath)


# ==================== Helper Function and Tools ========================
# !!!!!! Be mindful all the files under that dir will be deleted
# clean output image dir for new session
def clearImageDir(folder_path):
    files = glob.glob(folder_path + "*")
    for f in files:
        os.remove(f)


# Not being Used
def move_File_To_User_Upload(original, distnation):
    current = original
    newDistnation = distnation
    os.rename(current, newDistnation)


def execute_Box_Detection(path, blocks):
    imageOutputFileDirectory = newSession.getCropDir()
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
    #     print("========================================================================")


# Main
if __name__ == "__main__":
    # Initialize timer for run time speed
    start = time.time()
    # clearImageDir("/Users/edwardlai/Documents/2019 Spring Assignments/HTML_Forge/App/src/ImageProcessing/UserUpload/")

    # passToken(newsession.getSessionID())
    startSession(
        "/Users/edwardlai/Documents/2019 Spring Assignments/HTML_Forge/App/Sample Images/Sample_1.jpg")

    end = time.time()
    print("Process Run Time: Seconds: ", end - start)

# To-do
# [Done]  Reformat and resize the image to get consistent result and image crop
# [Done]  Crop image with the x, y, w, h adjust.
# [Done]  Save the crop of the source file instead of the bolded one
# [Done]  Remove similar crops
# [Done]  Image enhancer on the original Image
# [Done]  Uses child relationship and hierarchy to know the objects within each block
#               and eventually add it into single block attribute
# [Done]  JSON File Formatter
# [Done]  Image Drawing, boxing out detected labels
# [Done]  Full Image Path

# Need to fix
# [Done] Array index contour removal out of range
# [Done] Image Dir with sessions
# [In Progress] Keeping original image size and algo rescale with it
