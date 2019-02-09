# img = cv2.imread("/Users/edwardlai/Downloads/IMG_1533.JPG", 0)


import cv2
from imutils.contours import sort_contours

import numpy as np
import matplotlib.pyplot as plt


#This is just for the py plot display
fig = plt.figure(figsize=(8, 8))
columns = 4
rows = 4


def box_extraction(img_for_box_extraction_path, cropped_dir_path):
    img = cv2.imread(img_for_box_extraction_path, 0)  # Read the image

    (thresh, img_bin) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Threshold and contrast the image
    img_bin = cv2.resize(img_bin, (3000, 2000))

    img_bin = 255 - img_bin  # Invert the image

    cv2.imwrite("Image_bin.jpg", img_bin)



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
    cv2.imwrite("verticle_lines.jpg", verticle_lines_img)
    # Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=ITERATIONS)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=ITERATIONS)
    cv2.imwrite("horizontal_lines.jpg", horizontal_lines_img)



    #summation or two images
    alpha = 0.5
    beta = 1.0 - alpha
    img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=ITERATIONS)
    (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imwrite("img_final_bin.jpg", img_final_bin)

    # Find contours for image, which will detect all the boxes
    contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Sort all the contours by top to bottom.
    (contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")

    print("============================")
    print(hierarchy)
    print("============================")

    idx = 0
    for c in contours:
        # Returns the location and width,height for every contour
        x, y, w, h = cv2.boundingRect(c)
        # img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        print("the width: ", w)
        print("the height: ", h)
        print(w, " > the 3*h: ", 3*h )
        print("========================")
        # If the box height is greater then 700 or width is >700, then only save it as a box in "cropped/" folder.
        if ((w > 700 and h >30) or (h > 700 and w >30)) and w != 3000 and h != 2000:
            print("image Crop!")
            idx += 1
            new_img = img[y:y + h, x:x + w]
            fig.add_subplot(rows, columns, idx)
            plt.imshow(new_img)
            cv2.imwrite(cropped_dir_path + str(idx) + '.png', new_img)
        else:
            print("log: element too small" )
            print("===========================")
    plt.show()
    cv2.imshow('boxed', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


#call on an image with path and cropped output dir
box_extraction("houghlines5.jpg", "cropped/")
