from Blocks.Blocks import blocks, addBlock, getBlockByID
from imutils.contours import sort_contours
import cv2
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import time

from GoogleCloudServices.predictBlock import imageOnReady

Image_Debug = False
Console_Logger = True

# This is just for the py plotting results (debug purposes)
fig = plt.figure(figsize=(8, 8))
columns = 3
rows = 3

ITERATIONS = 0
TARESHOLD = 100
MIN_LINE_LENG = 100
MAX_LINE_GAP = 30
exported_contours = []


# 1
#  This will rescale all in user image into 3:2 Image ratio
def image_Rescale(image_Path):
    size = 3000, 2000
    from PIL import Image
    im = Image.open(image_Path)
    im.thumbnail(size)
    new_path = "User Upload/" + "_resized.jpg"
    im.save(new_path)
    return new_path


def cornerFit(imgPath):
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
    X_MIN = min(x_arr)
    X_MAX = max(x_arr)
    Y_MIN = min(y_arr)
    Y_MAX = max(y_arr)
    crop_img = img[Y_MIN - 200: Y_MAX + 200, X_MIN - 200: X_MAX + 200]
    # plt.imshow(crop_img), plt.show()
    cv2.imwrite("User Upload/" + "precrop.jpg", crop_img)


# Not being used
def enhanceImage(fileName):
    from PIL import Image, ImageEnhance
    im = Image.open("User Upload/" + fileName)
    # enhancer = ImageEnhance.Brightness(im)
    temp = ImageEnhance.Sharpness(im)
    enhanced_im = temp.enhance(10.0)
    enhanced_im.save("User Upload/" + "ENH_" + fileName)


# 2
# line_Balding function
# Param: a openCV Bin Image
# Return: Bolded openCV Bin Image
def line_Bolding(imgpath):
    img = cv2.imread(imgpath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 255, 255, apertureSize=3)
    if Image_Debug: cv2.imwrite('DebugImagesDir/cann.jpg', edges)

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
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 0), 3)

    cv2.imwrite('DebugImagesDir/houghlines5.jpg', img)
    cv2.destroyAllWindows()


# 3
# Function for box detection
def box_extraction(original_image_path, img_for_box_extraction_path, cropped_dir_path):
    orginal_image = cv2.imread(original_image_path, 0)

    img = cv2.imread(img_for_box_extraction_path, 0)  # Read the image
    # img = img_for_box_extraction_path
    # cv2.imshow(img)
    (thresh, img_bin) = cv2.threshold(img, 128, 255,
                                      cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Threshold and contrast the image
    img_bin = cv2.resize(img_bin, (3000, 2000))

    try:
        img_bin = 255 - img_bin  # Invert the image
    except:
        print("failed to invert")

    if Image_Debug: cv2.imwrite("DebugImagesDir/Image_bin.jpg", img_bin)

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
    if Image_Debug: cv2.imwrite("DebugImagesDir/verticle_lines.jpg", verticle_lines_img)
    # Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=ITERATIONS)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=ITERATIONS)
    if Image_Debug: cv2.imwrite("DebugImagesDir/horizontal_lines.jpg", horizontal_lines_img)

    # summation or two images
    alpha = 0.5
    beta = 1.0 - alpha
    img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=ITERATIONS)
    (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    if Image_Debug: cv2.imwrite("DebugImagesDir/img_final_bin.jpg", img_final_bin)

    # Find contours for image, which will detect all the boxes
    contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_LIST, cv2.CHAIN_APPRO)
    # Sort all the contours by top to bottom.
    (contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")
    # (contours, boundingBoxes) = sort_contours(contours, method="bottom-to-top")

    if Console_Logger: print("============ Hierarchy ================")
    if Console_Logger: print(hierarchy)
    if Console_Logger: print("============================")

    for c in contours:
        # Returns the location and width,height for every contour
        x, y, w, h = cv2.boundingRect(c)
        # if Console_Logger: print("width: ", w, "\theight:", h)
        # if Console_Logger: print("========================")
        # If the box height is greater then 700 or width is >700, then only save it as a box in "cropped/" folder.
        if ((w > 700 and h > 30) or (h > 700 and w > 30)) and w != 3000 and h != 2000 and x > 100 and y > 100:
            if Console_Logger: print("Crop Log: ", [x, y, w, h])
            exported_contours.append([x, y, w, h])

    # Iterate through final candidates and remove repetitive blocks
    for i in range(len(exported_contours) - 1, 0, -1):
        for j in range(i):
            # Compare X axis and Y see if it is similar crop
            DUPLICATE_TARESHOLD = 80
            # if abs(exported_contours[i][0] - exported_contours[j][0]) <= DUPLICATE_TARESHOLD and abs(
            #         exported_contours[i][1] - exported_contours[j][1]) <= DUPLICATE_TARESHOLD:
            # Similar item choose bigger frame and save to the list.
            temp_1 = abs(sum(exported_contours[i]))
            temp_2 = abs(sum(exported_contours[j]))
            # print(temp_1/ temp_2)
            if (temp_1 / temp_2) > 0.98 and (temp_1 / temp_2) < 1.05:
                if Console_Logger: print("Delete Log: Image Similar contour removed")
                # Choose the bigger contour and pop the smaller crop
                if ((exported_contours[j][2] + exported_contours[j][3]) > exported_contours[i][2] +
                        exported_contours[i][3]):
                    exported_contours.pop(j)
                else:
                    exported_contours.pop(i)

    if Console_Logger: print("============================")
    # Cropping image and create single block instances
    if Console_Logger: print("Final Exported Contours: ", exported_contours)

    idx = 0
    for i in range(0, len(exported_contours)):
        idx += 1
        x = exported_contours[i][0]
        y = exported_contours[i][1]
        w = exported_contours[i][2]
        h = exported_contours[i][3]

        # The crop is right is too tight since it is right on the border, this adjusts with bigger border
        x -= 350
        y -= 50
        w += 80
        h += 80

        # Cropping the original image
        new_img = orginal_image[y:y + h, x:x + w]

        cv2.imwrite(cropped_dir_path + str(idx) + '.png', new_img)
        createSingleBlockInstance(idx, x, y, h, w, cropped_dir_path + str(idx) + '.png')

        # Display cropped image onto the mlplot
        if Image_Debug: fig.add_subplot(rows, columns, idx)
        if Image_Debug: plt.imshow(new_img)

    if Image_Debug: plt.show()
    # if Image_Debug: cv2.imshow('boxed', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 3.5
# create all the detected blocks as single instance
def createSingleBlockInstance(id, x, y, h, w, sorcePath):
    addBlock()
    getBlockByID(id).setX_Location(x)
    getBlockByID(id).setY_Location(y)
    getBlockByID(id).set_Height(h)
    getBlockByID(id).set_Width(w)
    getBlockByID(id).setImagePath(sorcePath)


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


# file path must be in User Upload!
def execute_Box_Detection(fileName_mustBeInUserUpload):
    img = 'User Upload/' + fileName_mustBeInUserUpload
    imageOutputFileDirectory = "cropped/"
    # Delete images from previous session
    clearImageDir(imageOutputFileDirectory)
    # rescale image size to have more unified image to work with
    img = image_Rescale(img)
    # Analyze thin lines and enhance it
    line_Bolding(img)
    # Execute the block detection feature
    box_extraction(img, "DebugImagesDir/houghlines5.jpg", imageOutputFileDirectory)


# Main
if __name__ == "__main__":
    # Initialize timer for run time speed
    start = time.time()

    # enhanceImage("IMG_1554.JPG")

    # Image first got fed through corner detection for initial crop
    # This will get more unify result
    cornerFit("User Upload/Sample_1.jpg")
    # cornerFit("User Upload/ENH_IMG_1554.JPG")
    # cornerFit("User Upload/testimg.jpg")
    # cornerFit("User Upload/IMG_1536.JPG")

    # Pass in the pre cropped image for building block detection
    execute_Box_Detection("precrop.jpg")

    # All building block infos stored in blocks class
    # Call AI for further process
    # imageOnReady()

    end = time.time()
    print("Seconds: ", end - start)

# To-do
# [Done]  Reformat and resize the image to get consistent result and image crop
# [Done]  Crop image with the x, y, w, h adjust.
# [Done]  Save the crop of the source file instead of the bolded one
# [Done] Remove similar crops
# [IN Progress] Image enhancer on the original Image
# [Done] Uses child relationship and hierarchy to know the objects within each block
#               and eventually add it into single block attribute
