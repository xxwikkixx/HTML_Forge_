"""
    This script is the first step of image processing. It takes whatever image path and import for pre-processing.
    Storing all the detected hand drawings (building blocks) into blocks database.
    Then Crop the detected blocks and pass to AI fo image classification

    Implementation steps
        0. Move Image           - to local working environment and convert any images into JPEG extension
        1. Image Cropping Unify - applying unify crop to user image to have consistent edge detection
        2. Image enhancement    - Apply gaussian and contrast to the image
        3. Thin Line Repair     - Algorithm to fix thin lines and breaking lines in the image
        5. Erode and Dilate     - Algorithm to merge corners and disjointed drawings
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
         [Done]  Uses child relationship and hierarchy to know the objects within each block and eventually add it into
                single block attribute
         [Done]  JSON File Formatter
         [Done]  Image Drawing, boxing out detected labels
         [Done]  Full Image Path
         [Done]  Array index contour removal out of range
         [Done]  Image Dir with sessions
         [Done]  OpenCV Dilation and Erosion
         [Done]  Keeping original image size and algo rescale with it
         [Done]  Initial crop out of bound on tight images.
"""

from PIL import Image, ImageEnhance, ImageDraw, ImageFont, ImageStat
from predictBlock import imageOnReady
from ImgProcessSession import ImageProcessSession
from Blocks import Blocks
from imutils.contours import sort_contours
import cv2
import os
import glob
import numpy as np

# Set true if debugging
Image_Debug = False
Console_Logger = False
Disable_AI = False

# IMAGE_HEIGHT = 1000
# IMAGE_WIDTH = 1500

IMAGE_HEIGHT = 2000
IMAGE_WIDTH = 3000

# erode and dilate
ITERATIONS = 1

# For line bolding
TARESHOLD = 20
MIN_LINE_LENG = 15
MAX_LINE_GAP = 25

# Current script work environment
FULL_PATH_TO_THIS_FOLDER = (os.getcwd())


class boxDetection():
    def __init__(self):
        self.job = ImageProcessSession()
        self.imagePath = ""
        self.sessionID = self.job.getSessionID()
        self.blocksDB = Blocks()

    def setImagePath(self, path):
        self.imagePath = path

    def getImagePath(self):
        return self.imagePath

    def getSessionID(self):
        return self.sessionID


    def image_Rescale(self, image_Path):
        """
            This will rescale all in user image into 3:2 Image ratio
            Perform and save to the same image path

            :param image_Path: string : Path to image
        """
        size = IMAGE_HEIGHT, IMAGE_WIDTH
        im = Image.open(image_Path)
        im.thumbnail(size)
        newimg = im.resize(size)

        # newimg = newimg.point(lambda p: p * 1.5)
        # If the image if too dark

        if self.brightness(image_Path) < 100:
            print ("Level 1 Enhance ---> Apply Min")
            newimg = newimg.point(lambda p: p * 1.8)
        if self.brightness(image_Path) < 205:
            print ("Level 2 Enhance ---> Apply Mid")
            newimg = newimg.point(lambda p: p * 1.4)
        if self.brightness(image_Path) < 235:
            print ("Level 3 Enhance ---> Apply Strong")
            newimg = newimg.point(lambda p: p * 1.1)

        newimg.save(image_Path)

    def brightness(self, im_file):
        im = Image.open(im_file).convert('L')
        stat = ImageStat.Stat(im)
        return stat.mean[0]

    def applyGaussian(self, image_Path):
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
        T = threshold_adaptive(warped, 11, offset=10, method="gaussian")
        gray = (gray > T).astype("uint8") * 255
        # save image to the same image path
        cv2.imwrite(image_Path, gray)


    def fileConvert(self, imgPath, savePath):
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
        im = im.convert('L')
        im.save(savePath)

    def cornerFit(self, imgPath):
        """
            cornerFit detects the most outer corners and perform and tight crop around it.
            This will ensure better and more unified blx detection
            Perform and save to the same image path
        :param imgPath: path to the image
        """

        # applyGaussian(imgPath)

        # read the image
        img = cv2.imread(imgPath)

        # h, w, meh = img.shape
        # print("Height",h,"Width", w)
        # if w > h:
        #     print("Image Flipped")
        #     img = cv2.warpAffine(img, cv2.getRotationMatrix2D(((h / 2), (w / 2)), 270, 1.0), (h, w))
        #     cv2.imwrite("/Users/edwardlai/Documents/2019 Spring Assignments/HTML_Forge/App/test.jpg", img)
        #


        # convert image to gray scale image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # detect corners with the goodFeaturesToTrack function.
        # gray = cv2.GaussianBlur(gray, (15, 15), 20)
        corners = cv2.goodFeaturesToTrack(gray, 1000, 0.01, 15)
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

        if X_MIN - 100 >= 0 and Y_MIN - 100 >= 0:
            print ("Log: Initial Image Cropped")
            cv2.imwrite(imgPath, img[Y_MIN - 100: Y_MAX + 100, X_MIN - 100: X_MAX + 100])
        else:
            # User upload Image are too tight, do not perform crop and save the original one
            print("Warning: Edge are tight, rescale crop can not be performmed")
            cv2.imwrite(imgPath, img)

        # plt.imshow(img), plt.show()
        # plt.imshow(crop_img), plt.show()

    # Not being used
    def enhanceImage(self, path):
        im = Image.open(path)
        # enhancer = ImageEnhance.Brightness(im)
        temp = ImageEnhance.Sharpness(im)
        enhanced_im = temp.enhance(10.0)
        enhanced_im.save(path)

    def line_Bolding(self, imgpath):
        """
            line_Balding function takes an image path and draw lines to places where if the user drawings' line are too thin
            :param imgpath: string Path to the image
        """

        img = cv2.imread(imgpath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Canny function to enhance edges
        edges = cv2.Canny(gray, 255, 255, apertureSize=3)
        if Image_Debug: cv2.imwrite(self.job.getDebugDir() + 'cann.jpg', edges)

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

        cv2.imwrite(self.job.getDebugDir() + 'houghlines.jpg', img)  # For debug use
        # cv2.imwrite(imgpath, img)
        cv2.destroyAllWindows()

    def box_extraction(self, original_image_path, img_for_box_extraction_path, cropped_dir_path, blocks):
        """
            Function for Hand drawn Box Detection
            Detects Blocks, remove similar crops, apply crops, and store detected blocks

        :param original_image_path: string              Original Image
        :param img_for_box_extraction_path: string      Image with all the enhancements
        :param cropped_dir_path: string                 The detected and crops' output folder
        :param blocks: Object                           Block class instance to store all the detected information
        :return:
        """
        # clear array
        exported_contours = []
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

        if Image_Debug: cv2.imwrite(self.job.getDebugDir() + "Image_bin.jpg", img_bin)

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
        if Image_Debug: cv2.imwrite(self.job.getDebugDir() + "verticle_lines.jpg", verticle_lines_img)
        cv2.imwrite(self.job.getDebugDir() + "verticle_lines.jpg", verticle_lines_img)

        # Morphological operation to detect horizontal lines from an image
        img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=ITERATIONS)
        horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=ITERATIONS)
        # if Image_Debug: cv2.imwrite(self.job.getDebugDir() + "horizontal_lines.jpg", horizontal_lines_img)
        cv2.imwrite(self.job.getDebugDir() + "horizontal_lines.jpg", horizontal_lines_img)
        # summation or two images
        alpha = 0.5
        beta = 1.0 - alpha
        img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
        img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
        img_final_bin = cv2.dilate(~img_final_bin, kernel, iterations=2)
        # img_final_bin = cv2.dilate(~img_final_bin, kernel, iterations=)
        (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # if Image_Debug: cv2.imwrite(self.job.getDebugDir() + "img_final_bin.jpg", img_final_bin)
        cv2.imwrite(self.job.getDebugDir() + "img_final_bin.jpg", img_final_bin)
        # Find contours for image, which will detect all the boxes
        contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_LIST, cv2.CHAIN_APPRO)
        # Sort all the contours by top to bottom.

        (contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")

        # print ("=====>", hierarchy)
        # (contours, boundingBoxes) = sort_contours(contours, method="bottom-to-top")

        # if Console_Logger: print("============ Hierarchy ================")
        # if Console_Logger: print(hierarchy)
        # if Console_Logger: print("=======================================")

        # Find the suitable crops
        for c in contours:
            # Returns the location and width,height for every contour
            x, y, w, h = cv2.boundingRect(c)
            if ((w > IMAGE_WIDTH * 0.2 and h > IMAGE_HEIGHT * 0.07) or (
                    h > IMAGE_HEIGHT * 0.2 and w > IMAGE_WIDTH * 0.07)) and w != IMAGE_HEIGHT and h != IMAGE_WIDTH and x > 10 and y > 10:
                if Console_Logger: print("Crop Log: ", [x, y, w, h])
                # Add all the suitable crops to a list

                if len(exported_contours) == 0:
                    exported_contours.append([x, y, w, h])

                flag = True
                for i in range(0, len(exported_contours)):
                    x1, y1, w1, h1 = exported_contours[i]
                    x2, y2, w2, h2 = x, y, w, h

                    # Checks most instant sized similar crop
                    temp_1, temp_2 = float(abs(sum(exported_contours[i]))), float(abs(x + y + w + h))
                    if 0.93 < temp_1 / temp_2 < 1.08:
                        flag = False  # Dont include to the final contour

                    # This removes the inner children, and leaves with the most outer crop
                    if x2 > x1 and y2 > y1:  # Top left corner check
                        if x1 + w1 > x2 + w2:  # Top right corner check
                            if y1 + h1 > y2 + h2:  # Bottom Left corner check
                                # At this point (x2,y2) contour is inside (x1, y1) contour
                                flag = False

                    # Lay over Area
                    Box_1 = x1 * y1
                    Box_2 = x2 * y2

                    # if 1 > abs(Box_1 / Box_2) > 0.5:
                    #     print (abs(Box_1/Box_2))

                # If passing all the above cases we can now add it to the crop queue
                if flag: exported_contours.append([x, y, w, h])

        if Console_Logger: print("============================")
        # Start cropping image and create single block instances
        print (str(len(exported_contours)) + " Objects Detected: ", exported_contours)
        if Console_Logger: print("Final Exported Contours: ", exported_contours)
        idx = 0
        for i in range(0, len(exported_contours)):
            idx += 1
            x, y, w, h = exported_contours[i]

            # The crop is right is too tight, since it is right on the border, this adjusts with bigger border
            # And ensure the crop is within the page size
            if x - 80 > 0 and y - 80 > 0 and y + h + 110 < IMAGE_HEIGHT and x + w + 110 < IMAGE_WIDTH:
                x -= 80
                y -= 80
                w += 110
                h += 110
            # Cropping the original image
            new_img = orginal_image[y:y + h, x:x + w]

            # Save to assigned path
            cv2.imwrite(cropped_dir_path + str(idx) + '.png', new_img)

            # Create a Single Block Instance and add Single Block to Blocks Database
            self.createSingleBlockInstance(blocks, idx, x, y, h, w, cropped_dir_path + str(idx) + '.png')

            # Display cropped image onto the mlplot
            # if Image_Debug: fig.add_subplot(rows, columns, idx)
            # if Image_Debug: plt.imshow(new_img)

        # if Image_Debug: plt.show()
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def createSingleBlockInstance(self, blocks, id, x, y, h, w, sorcePath):
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
    def clearImageDir(self, folder_path):
        """
         !!!!!! Be mindful all the files under that dir will be deleted
         clean output image dir for new session

        :param folder_path: String  Path to the Dir you want to remove all the file
        """
        files = glob.glob(folder_path + "*")
        for f in files:
            os.remove(f)

    def execute_Box_Detection(self, path, blocks):
        """
        Helper Function of steps processing the box detection

        :param path: String Path the image for processing
        :param blocks: Object  Object Block Class instance to store detected boxes
        :return:
        """
        # Delete images from previous session
        # clearImageDir(imageOutputFileDirectory)

        # rescale image size to have more unified image to work with
        self.image_Rescale(path)

        # Analyze thin lines and enhance it
        self.line_Bolding(path)

        # Execute the block detection feature

        # @params:[original image path, enhancedImagePath, exportImageDir]
        cp_Dir = self.job.getCropDir()
        self.box_extraction(path, self.job.getDebugDir() + 'houghlines.jpg', cp_Dir, blocks)

    # Once the AI is finished, draw the detected boxes on to the original image
    def labelDrawBox(self, blocks, src):
        """
        Draw layering boxes on to the original image. The output image gives a good over look of what is detected and what is not

        :param blocks: Object BlockDB Class instance
        :param src: String Image destination
        :return: N/A
        """
        source_img = Image.open(src)
        draw = ImageDraw.Draw(source_img)
        # font = ImageFont.load_default().font
        font = ImageFont.truetype(FULL_PATH_TO_THIS_FOLDER + "/arial.ttf", 42)
        for i in blocks.blocks:
            x = blocks.getBlockByID(i).getX_Location()
            y = blocks.getBlockByID(i).getY_Location()
            w = blocks.getBlockByID(i).get_Width()
            h = blocks.getBlockByID(i).get_Height()

            draw.rectangle(((x, y), (x + w, y + h)), outline="red", width=4)

            draw.text((x + 10, y), str(blocks.getBlockByID(i).getBestPrediction()), fill="red", font=font)
        # source_img.show()
        source_img.save(src, "JPEG")

    # def initializeSession(self):
    #     """
    #     Scrip to start a new session instance.
    #     In each session from user it creates a folder in local database for storing crop img codes, and original images
    #     :return: String Session ID of the newly created session
    #     """

        # self.sessionID = ImageProcessSession()
        # return self.sessionID.getSessionID()

    def startSession(self, path_to_image):
        """
        The main script/steps for running the object detection

        :param path_to_image: String Path to the userInput image.
        :return: SessionID, and path to the JSON file. JSON
                file contains all the information we have regard each building blocks
        """

        print (path_to_image)

        self.job.userImageImport(path_to_image)

        # Initialize a new session base on user's request
        imgName = self.job.getSessionID() + ".jpg"
        self.fileConvert(self.job.getpathToUserImage(), self.job.getSessionPath() + "/" + imgName)

        # Image first got fed through corner detection for initial crop [This will get more unify result]
        self.cornerFit(self.job.getSessionPath() + "/" + imgName)



        # Pass in the pre cropped image for building block detection
        self.execute_Box_Detection(self.job.getSessionPath() + "/" + imgName, self.blocksDB)

        # ===============================
        #   AI PASS THROUGH
        # ===============================
        # All building block infos stored in blocks class
        # Call AI for further process
        if not Disable_AI:
            imageOnReady(self.blocksDB)

        self.labelDrawBox(self.blocksDB, self.job.getSessionPath() + imgName)
        self.blocksDB.JSONFormat(self.job.getSessionPath() + "/" + "data.json", self.job.getSessionID())

        return self.job.getSessionID(), self.job.getSessionPath() + "data.json"
