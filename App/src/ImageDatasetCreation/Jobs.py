import itertools
import random
from PIL import Image

from MergeTool import dirFiles, checkAllRescale, findCenterXY, scaleByRatio
from ImageCons import ImageCons


# from App.src.ImageDatasetCreation.MergeTool import scaleByRatio


def structLeftImageBox():
    # session = [dirFiles("OuterBox"), dirFiles("Image"), dirFiles("Text")]
    session = [dirFiles("OuterBox"), dirFiles("PersonImage"), dirFiles("Text")]  # Person Images
    que_List = list(itertools.product(*session))
    # print(que_List)

    for i in range(0, 200):
        rand = random.randint(1, len(que_List))

        try:
            OuterBox = Image.open(que_List[rand][0])
            IMG = Image.open(que_List[rand][1])
            Text = Image.open(que_List[rand][2])
        except IOError:
            print("Error")

        # Initial the Outer Box
        temp = ImageCons(OuterBox.size)
        temp.setBase(OuterBox.size[0], OuterBox.size[1])
        image_copy = OuterBox.copy()

        # Process IMG
        temp.setTarget(IMG.size[0], IMG.size[1])
        # IMG = scaleByRatio(IMG, temp, 0.6)
        IMG = checkAllRescale(IMG, temp)
        image_copy.paste(IMG, findCenterXY(temp.LEFT, temp))

        temp.setTarget(Text.size[0], Text.size[1])
        Text = checkAllRescale(Text, temp)
        image_copy.paste(Text, findCenterXY(temp.RIGHT, temp))

        image_copy.save("Output/IMG_Left_Text_Right/" + str(i) + ".png")


def structRightImageBox():
    # session = [dirFiles("OuterBox"), dirFiles("Image"), dirFiles("Text")]
    session = [dirFiles("OuterBox"), dirFiles("PersonImage"), dirFiles("Text")]  # Person Images
    que_List = list(itertools.product(*session))
    # print(que_List)

    for i in range(0, 200):
        rand = random.randint(0, len(que_List))

        try:
            OuterBox = Image.open(que_List[rand][0])
            IMG = Image.open(que_List[rand][1])
            Text = Image.open(que_List[rand][2])
        except IOError:
            print("Error")

        # Initial the Outer Box
        temp = ImageCons(OuterBox.size)
        temp.setBase(OuterBox.size[0], OuterBox.size[1])
        image_copy = OuterBox.copy()

        # Process IMG
        temp.setTarget(IMG.size[0], IMG.size[1])
        # IMG = scaleByRatio(IMG, temp, 0.6)
        IMG = checkAllRescale(IMG, temp)
        image_copy.paste(IMG, findCenterXY(temp.RIGHT, temp))

        temp.setTarget(Text.size[0], Text.size[1])
        Text = checkAllRescale(Text, temp)
        image_copy.paste(Text, findCenterXY(temp.CENTER, temp))

        image_copy.save("Output/IMG_Right_Text_Left/" + str(i) + ".png")


def structCenterImageBox():
    # session = [dirFiles("OuterBox"), dirFiles("Image"), dirFiles("Text")]
    session = [dirFiles("OuterBox"), dirFiles("PersonImage"), dirFiles("Text")]  # Person Images
    que_List = list(itertools.product(*session))
    # print(que_List)

    for i in range(0, 200):
        print(i)
        rand = random.randint(1, len(que_List))

        try:
            OuterBox = Image.open(que_List[rand][0])
            IMG = Image.open(que_List[rand][1])
            Text = Image.open(que_List[rand][2])
        except IOError:
            print("Error")

        # Initial the Outer Box
        temp = ImageCons(OuterBox.size)
        temp.setBase(OuterBox.size[0], OuterBox.size[1])
        image_copy = OuterBox.copy()

        # Process IMG
        temp.setTarget(IMG.size[0], IMG.size[1])
        # IMG = scaleByRatio(IMG, temp, 0.6)
        IMG = checkAllRescale(IMG, temp)
        image_copy.paste(IMG, findCenterXY(temp.CENTER, temp))

        temp.setTarget(Text.size[0], Text.size[1])
        Text = checkAllRescale(Text, temp)
        image_copy.paste(Text, findCenterXY(temp.CENTER_BOTTOM, temp))

        image_copy.save("Output/IMG_Top_Text_Bottom/" + str(i) + ".png")


def plainImageGallary():
    session = [dirFiles("OuterBox"), dirFiles("Image")]
    que_List = list(itertools.product(*session))
    # print(que_List)

    for i in range(0, 200):
        print(i)
        rand = random.randint(1, len(que_List))

        try:
            OuterBox = Image.open(que_List[rand][0])
            IMG = Image.open(que_List[rand][1])
        except IOError:
            print("Error")

        # Initial the Outer Box
        temp = ImageCons(OuterBox.size)
        temp.setBase(OuterBox.size[0], OuterBox.size[1])
        image_copy = OuterBox.copy()

        # Process IMG
        temp.setTarget(IMG.size[0], IMG.size[1])
        IMG = checkAllRescale(IMG, temp)
        image_copy.paste(IMG, findCenterXY(temp.TOP_LEFT, temp))
        image_copy.paste(IMG, findCenterXY(temp.LEFT, temp))
        image_copy.paste(IMG, findCenterXY(temp.BOTTOM_LEFT, temp))
        image_copy.paste(IMG, findCenterXY(temp.CENTER_TOP, temp))
        image_copy.paste(IMG, findCenterXY(temp.CENTER, temp))
        image_copy.paste(IMG, findCenterXY(temp.CENTER_BOTTOM, temp))
        image_copy.paste(IMG, findCenterXY(temp.TOP_RIGHT, temp))
        image_copy.paste(IMG, findCenterXY(temp.RIGHT, temp))
        image_copy.paste(IMG, findCenterXY(temp.BOTTOM_RIGHT, temp))
        image_copy.save("Output/Plain_Image_Gallary/" + str(i) + ".png")


# Image Flip

def imageFlip():
    session = [dirFiles("OuterBox"), dirFiles("Image"), dirFiles("LeftArrow"), dirFiles("RightArrow")]
    que_List = list(itertools.product(*session))
    # print(que_List)

    for i in range(0, 200):
        print(i)
        rand = random.randint(1, len(que_List))

        try:
            OuterBox = Image.open(que_List[rand][0])
            IMG = Image.open(que_List[rand][1])
            LeftArrow = Image.open(que_List[rand][2])
            RightArrow = Image.open(que_List[rand][3])
        except IOError:
            print("Error")

        # Initial the Outer Box
        temp = ImageCons(OuterBox.size)
        temp.setBase(OuterBox.size[0], OuterBox.size[1])
        OuterLayer = OuterBox.copy()

        # Process IMG
        temp.setTarget(IMG.size[0], IMG.size[1])
        # IMG = scaleByRatio(IMG, temp, 0.6)
        IMG = checkAllRescale(IMG, temp)
        OuterLayer.paste(IMG, findCenterXY(temp.CENTER, temp))

        print(LeftArrow.size)
        temp.setTarget(LeftArrow.size[0], LeftArrow.size[1])
        LeftArrow = checkAllRescale(LeftArrow, temp)
        OuterLayer.paste(LeftArrow, findCenterXY(temp.LEFT, temp))

        print(LeftArrow.size)
        temp.setTarget(RightArrow.size[0], RightArrow.size[1])
        RightArrow = checkAllRescale(RightArrow, temp)
        OuterLayer.paste(RightArrow, findCenterXY(temp.RIGHT, temp))

        # temp.setTarget(Text.size[0], Text.size[1])
        # Text = checkAllRescale(Text, temp)
        # image_copy.paste(Text, findCenterXY(temp.CENTER_BOTTOM, temp))

        OuterLayer.save("Output/Image_Flip/" + str(i) + ".png")

        OuterLayer.close()
        IMG.close()
        LeftArrow.close()
        RightArrow.close()


# Image Flip with preview
def imageFlip():
    session = [dirFiles("OuterBox"), dirFiles("Image"), dirFiles("LeftArrow"), dirFiles("RightArrow"),
               dirFiles("GallaryBottom")]
    que_List = list(itertools.product(*session))
    # print(que_List)

    for i in range(0, 200):
        print(i)
        rand = random.randint(1, len(que_List))

        try:
            OuterBox = Image.open(que_List[rand][0])
            IMG = Image.open(que_List[rand][1])
            LeftArrow = Image.open(que_List[rand][2])
            LeftArrow.thumbnail((200, 200))

            RightArrow = Image.open(que_List[rand][3])
            RightArrow.thumbnail((200, 200))

            GallaryBottom = Image.open(que_List[rand][4])
            GallaryBottom.thumbnail((400, 1000))

        except IOError:
            print("Error")

        # Initial the Outer Box
        temp = ImageCons(OuterBox.size)
        temp.setBase(OuterBox.size[0], OuterBox.size[1])
        OuterLayer = OuterBox.copy()

        # Process IMG
        temp.setTarget(IMG.size[0], IMG.size[1])
        # IMG = scaleByRatio(IMG, temp, 0.6)
        IMG = checkAllRescale(IMG, temp)
        OuterLayer.paste(IMG, findCenterXY(temp.CENTER, temp))

        print(LeftArrow.size)
        temp.setTarget(LeftArrow.size[0], LeftArrow.size[1])
        # LeftArrow = checkAllRescale(LeftArrow, temp)
        # GallaryBottom = scaleByRatio(GallaryBottom, temp, 1.3)
        OuterLayer.paste(LeftArrow, findCenterXY(temp.LEFT, temp))

        print(LeftArrow.size)
        temp.setTarget(RightArrow.size[0], RightArrow.size[1])
        # RightArrow = checkAllRescale(RightArrow, temp)
        # GallaryBottom = scaleByRatio(GallaryBottom, temp, 1.3)
        OuterLayer.paste(RightArrow, findCenterXY(temp.RIGHT, temp))

        temp.setTarget(GallaryBottom.size[0], GallaryBottom.size[1])
        # GallaryBottom = checkAllRescale(GallaryBottom, temp)
        # GallaryBottom = scaleByRatio(GallaryBottom, temp, 1.4)
        OuterLayer.paste(GallaryBottom, findCenterXY(temp.CENTER_BOTTOM, temp))

        OuterLayer.save("Output/ImageFlipWithPreview/" + str(i) + ".png")

        OuterLayer.close()
        IMG.close()
        LeftArrow.close()
        RightArrow.close()
        GallaryBottom.close()


# List
# Header
# Footer
# Text

imageFlip()
# plainImageGallary()
# structRightImageBox()
# structLeftImageBox()
# structCenterImageBox()
