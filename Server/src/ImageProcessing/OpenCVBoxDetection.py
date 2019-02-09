import cv2
from imutils.contours import sort_contours
import os
import glob
import numpy as np
import matplotlib.pyplot as plt

Image_Debug = False
Console_Logger = False

# This is just for the py plot display (debug purposes)
fig = plt.figure(figsize=(8, 8))
columns = 4
rows = 4


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


def box_extraction(img_for_box_extraction_path, cropped_dir_path):
    img = cv2.imread(img_for_box_extraction_path, 0)  # Read the image
    # img = img_for_box_extraction_path
    # cv2.imshow(img)
    (thresh, img_bin) = cv2.threshold(img, 128, 255,
                                      cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Threshold and contrast the image
    img_bin = cv2.resize(img_bin, (3000, 2000))

    # img = line_Bolding(cv2.imread(img_for_box_extraction_path, 0))

    img_bin = 255 - img_bin  # Invert the image

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
            exported_contours.append([x, y, w, h])
        else:
            if Console_Logger: print("log: element too small")
            if Console_Logger: print("===========================")

    for i in range(len(exported_contours) - 1, 0, -1):
        for j in range(i):
            if Console_Logger: print(exported_contours[i][0])
            if abs(exported_contours[i][0] - exported_contours[j][0]) <= 50 and abs(
                    exported_contours[i][1] - exported_contours[j][1]) <= 50:
                # Similar item choose bigger frame and save to the list.
                if Console_Logger: print("First Condition")
                if ((exported_contours[j][2] + exported_contours[j][3]) > exported_contours[i][2] +
                        exported_contours[i][3]):
                    exported_contours.pop(i)

    if Console_Logger: print(exported_contours)
    idx = 0
    for i in range(0, len(exported_contours)):
        idx += 1
        x = exported_contours[i][0]
        y = exported_contours[i][1]
        w = exported_contours[i][2]
        h = exported_contours[i][3]
        new_img = img[y:y + h, x:x + w]
        fig.add_subplot(rows, columns, idx)
        plt.imshow(new_img)
        cv2.imwrite(cropped_dir_path + str(idx) + '.png', new_img)

    if Image_Debug: plt.show()
    if Image_Debug: cv2.imshow('boxed', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# call on an image with path and cropped output dir
def demo():
    img = 'User Upload/IMG_1536.JPG'
    imageOutputFileDirectory = "cropped/"

    # Delete images from previous session
    files = glob.glob(imageOutputFileDirectory + "*")
    for f in files:
        os.remove(f)

    line_Bolding(img)
    box_extraction("DebugImagesDir/houghlines5.jpg", imageOutputFileDirectory)


demo()
