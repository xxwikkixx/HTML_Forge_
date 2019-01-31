from PIL import Image
import os
import glob


class ImageProcessing:
    def __init__(self):
        self.blockID = 0
        self.imageOutputFileDirectory = "Processed Images/"
        self.imageSourceDirectory = "User Upload/userUpload.jpg"  # The source of the user image.

        self.leftBorder = 0
        self.upBorder = 0
        self.rightBorder = 0
        self.bottomBorder = 0

    def cleanImageDir(self):
        files = glob.glob(self.imageOutputFileDirectory + "*")
        for f in files:
            os.remove(f)

    def setImageFilePath(self, img):
        self.imageSourceDirectory = img

    def setImageID(self, imgID):
        self.blockID = imgID

    def setArea(self, left, up, right, bottom):
        self.leftBorder = left
        self.upBorder = up
        self.rightBorder = right
        self.bottomBorder = bottom

    def userUpload(self, path):
        current = path
        newDestnation = "User Upload/userUpload.jpg"
        os.rename(current, newDestnation)

    def cropImg(self):
        img = Image.open(self.imageSourceDirectory)
        area = (
            self.leftBorder, self.upBorder, self.rightBorder, self.bottomBorder)  # set all image crop area variables
        cropped_img = img.crop(area)
        cropped_img.show()  # Disable this later on
        cropped_img.save(self.imageOutputFileDirectory + str(self.blockID) + ".jpg")

        # return img

    def applyContrastAndMono(self):
        img = Image.open(self.imageSourceDirectory)
        level = 50
        factor = (259 * (level + 255)) / (255 * (259 - level))

        def contrast(c):
            return 128 + factor * (c - 128)

        contrastImg = img.point(contrast)
        monochromeImg = contrastImg.convert('1')

        monochromeImg.save(self.imageOutputFileDirectory + "Contrast and Mono Applied.jpg")

        # return monochromeImg

def runExample():
    imgCrop = ImageProcessing()
    imgCrop.cleanImageDir()  # Clean/ delete old images from last session
    imgCrop.setImageID(3)  # This should match the block ID
    imgCrop.setArea(250, 40, 800, 600)  # Crop Area
    imgCrop.cropImg()  # Perform crop and save
    imgCrop.applyContrastAndMono()


runExample()
