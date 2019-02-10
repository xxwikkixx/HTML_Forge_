import cv2
from imutils.contours import sort_contours
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from src.Blocks.Blocks import addBlock, getBlockByID, blocks
import multiprocessing as mp
import time

Image_Debug = True
Console_Logger = True

# This is just for the py plotting results (debug purposes)
fig = plt.figure(figsize=(8, 8))
columns = 4
rows = 4

# Not being used
def enhanceImage(fileName):
    from PIL import Image, ImageEnhance
    im = Image.open("User Upload/" + fileName)
    # enhancer = ImageEnhance.Brightness(im)
    temp = ImageEnhance.Sharpness(im)
    enhanced_im = temp.enhance(10.0)
    enhanced_im.save("User Upload/" + fileName)

# 3.5
def createSingleBlockInstance(id, x, y, h, w, sorcePath):
    addBlock()
    getBlockByID(id).setX_Location(x)
    getBlockByID(id).setY_Location(y)
    getBlockByID(id).set_Height(h)
    getBlockByID(id).set_Width(w)
    getBlockByID(id).setImagePath(sorcePath)

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
    lines = cv2.HoughLinesP(edges, rho=1, theta=1 * np.pi / 180, threshold=20, minLineLength=150, maxLineGap=30)

    if Console_Logger: print(len(lines))

    for i in range(0, len(lines)):
        x1, y1, x2, y2 = lines[i][0]
        if Console_Logger: print(x1, y1, x2, y2)

        # Draw the thicker black line on to the image
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 0), 8)

    cv2.imwrite('DebugImagesDir/houghlines5.jpg', img)
    cv2.destroyAllWindows()

# 3
def box_extraction(original_image_path, img_for_box_extraction_path, cropped_dir_path):
    orginal_image = cv2.imread(original_image_path, 0)

    img = cv2.imread(img_for_box_extraction_path, 0)  # Read the image
    # img = img_for_box_extraction_path
    # cv2.imshow(img)
    (thresh, img_bin) = cv2.threshold(img, 128, 255,
                                      cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Threshold and contrast the image
    img_bin = cv2.resize(img_bin, (3000, 2000))

    # img = line_Bolding(cv2.imread(img_for_box_extraction_path, 0))
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

    ITERATIONS = 1
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
    # Sort all the contours by top to bottom.
    (contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")

    if Console_Logger: print("============================")
    if Console_Logger: print(hierarchy)
    if Console_Logger: print("============================")

    exported_contours = []
    idx = 0
    for c in contours:
        # Returns the location and width,height for every contour
        x, y, w, h = cv2.boundingRect(c)
        # img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if Console_Logger: print("the width: ", w)
        if Console_Logger: print("the height: ", h)
        if Console_Logger: print(w, " > the 3*h: ", 3 * h)
        if Console_Logger: print("========================")
        # If the box height is greater then 700 or width is >700, then only save it as a box in "cropped/" folder.
        if ((w > 700 and h > 30) or (h > 700 and w > 30)) and w != 3000 and h != 2000:
            if Console_Logger: print("image Crop!")
            print(x, y, w, h)
            exported_contours.append([x, y, w, h])
        else:
            if Console_Logger: print("log: element too small")
            if Console_Logger: print("===========================")

    # Iterate through final canadians and remove repetitive blocks
    for i in range(len(exported_contours) - 1, 0, -1):
        for j in range(i):
            if Console_Logger: print(exported_contours[i][0])
            # Compare X axis and Y see if it is similar crop
            if abs(exported_contours[i][0] - exported_contours[j][0]) <= 80 and abs(
                    exported_contours[i][1] - exported_contours[j][1]) <= 80:
                # Similar item choose bigger frame and save to the list.
                if Console_Logger: print("First Condition")

                # Choose the bigger crop and pop the smaller one
                if ((exported_contours[j][2] + exported_contours[j][3]) > exported_contours[i][2] +
                        exported_contours[i][3]):
                    exported_contours.pop(i)

    print("============")
    # Cropping image and create single block instances
    if Console_Logger: print(exported_contours)
    idx = 0
    for i in range(0, len(exported_contours)):
        idx += 1
        x = exported_contours[i][0]
        y = exported_contours[i][1]
        w = exported_contours[i][2]
        h = exported_contours[i][3]

        # The crop is right is too tight since it is right on the border, this adjusts with bigger border
        x -= 200
        y -= 80
        w += 100
        h += 80

        print(x, y, w, h)
        # Cropping the original image
        new_img = orginal_image[y:y + h, x:x + w]

        try:
            cv2.imwrite(cropped_dir_path + str(idx) + '.png', new_img)
            createSingleBlockInstance(idx, x, y, h, w, cropped_dir_path + str(idx) + '.png')
        except:
            exported_contours.pop(i)
            print("error")
            continue

        # Display cropped image onto the matplot
        if Image_Debug: fig.add_subplot(rows, columns, idx)
        if Image_Debug: plt.imshow(new_img)

    if Image_Debug: plt.show()
    # if Image_Debug: cv2.imshow('boxed', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


### !!!!!! Be mindful all the files under that dir will be deleted
def clearImageDir(folder_path):
    files = glob.glob(folder_path + "*")
    for f in files:
        os.remove(f)

# 1
def image_Rescale(image_Path):
    size = 3000, 2000
    from PIL import Image
    im = Image.open(image_Path)
    im.thumbnail(size)
    new_path = "User Upload/" + "_resized.jpg"
    im.save(new_path)
    return new_path

# Not being Used
def move_File_To_User_Upload(original, distnation):
    current = original
    newDistnation = distnation
    os.rename(current, newDistnation)


# file path must be in User Upload!
def execute_Box_Detection(fileName_mustBeInUserUpload):
    # file_name = "IMG_1450
    # move_File_To_User_Upload(fileName_mustBeInUserUpload, "'User Upload/userUpload.jpg")

    pool = mp.Pool()

    img = 'User Upload/' + fileName_mustBeInUserUpload
    imageOutputFileDirectory = "cropped/"


    # Delete images from previous session
    clearImageDir(imageOutputFileDirectory)

    img = image_Rescale(img)
    line_Bolding(img)

    # pool.map(box_extraction, [img, "DebugImagesDir/houghlines5.jpg", imageOutputFileDirectory])
    box_extraction(img, "DebugImagesDir/houghlines5.jpg", imageOutputFileDirectory)
    # box_extraction(img, imageOutputFileDirectory)


    if Console_Logger:
        print("==================Image Cropping Create Single Blocks=====================")
        print(blocks)

        for i in blocks:
            print("Block ", i, " ID: :", getBlockByID(i).getBlockID())
            print("Block ", i, "  X Location: :", getBlockByID(i).getX_Location())
            print("Block ", i, "  Y Location: :", getBlockByID(i).getY_Location())
            print("Block ", i, "  Width: :", getBlockByID(i).get_Width())
            print("Block ", i, "  Height: :", getBlockByID(i).get_Height())
            print("Block ", i, "  image path: :", getBlockByID(i).getImagePath())
            print("========================================================================")


if __name__ == "__main__":
    start = time.time()

    # pool = mp.Pool()
    # pool.map_async(execute_Box_Detection, ["IMG_1536.JPG"])

    execute_Box_Detection("IMG_1536.JPG")


    print("Done")
    end = time.time()
    print("Seconds: ", end-start)

# To-do
# [Done]  Reformat and resize the image to get consistent result and image crop
# [Done]  Crop image with the x, y, w, h adjust.
# [Done]  Save the crop of the source file instead of the bolded one
# [In Progress] Image enhancer on the original Image
