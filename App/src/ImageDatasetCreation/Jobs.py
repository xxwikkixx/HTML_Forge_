import itertools
import random
from PIL import Image

from MergeTool import dirFiles, checkAllRescale, findCenterXY, scaleByRatio, checkHeightRescale
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
# Image Flip with preview
def header():
    session = [dirFiles("AllBoarders"), dirFiles("Image"), dirFiles("ClickableImage"), dirFiles("MenuDropDown"),
               dirFiles("SmallImage")]
    que_List = list(itertools.product(*session))
    # print(que_List)

    for i in range(0, 200):
        print(i)
        rand = random.randint(1, len(que_List))

        try:
            BannerBorder = Image.open(que_List[rand][0])
            IMG = Image.open(que_List[rand][1])

            ClickableImage = Image.open(que_List[rand][2])
            # ClickableImage.thumbnail((200, 200))

            MenuDropDown = Image.open(que_List[rand][3])
            MenuDropDown.thumbnail((100, 100))

            SmallImage = Image.open(que_List[rand][4])
            SmallImage.thumbnail((400, 400))

        except IOError:
            print("Error")

        # Initial the Outer Box
        temp = ImageCons(BannerBorder.size)
        temp.setBase(BannerBorder.size[0], BannerBorder.size[1])
        BannerLayer = BannerBorder.copy()

        # Process IMG
        temp.setTarget(IMG.size[0], IMG.size[1])
        # IMG = scaleByRatio(IMG, temp, 0.6)
        IMG = checkAllRescale(IMG, temp, 8)
        BannerLayer.paste(IMG, findCenterXY(temp.LEFT, temp))

        temp.setTarget(ClickableImage.size[0], ClickableImage.size[1])
        ClickableImage = checkAllRescale(ClickableImage, temp)
        # GallaryBottom = scaleByRatio(ClickableImage, temp, 1.3)
        # BannerLayer.paste(ClickableImage, findCenterXY(temp.RIGHT, temp))
        # BannerLayer.paste(ClickableImage, findCenterXY(temp.CENTER, temp))

        temp.setTarget(MenuDropDown.size[0], MenuDropDown.size[1])
        # MenuDropDown = checkAllRescale(MenuDropDown, temp)
        # GallaryBottom = scaleByRatio(MenuDropDown, temp, 1.3)
        BannerLayer.paste(MenuDropDown, findCenterXY(temp.RIGHT, temp))

        temp.setTarget(SmallImage.size[0], SmallImage.size[1])
        GallaryBottom = checkAllRescale(SmallImage, temp)
        # GallaryBottom = scaleByRatio(SmallImage, temp, 1.4)
        # BannerLayer.paste(SmallImage, findCenterXY(temp.CENTER, temp))

        BannerLayer.save("Output/Header/" + str(i) + ".png")

        # BannerLayer.close()
        # IMG.close()
        # ClickableImage.close()
        # MenuDropDown.close()
        # SmallImage.close()


# Footer
# List
# Header
# Image Flip with preview
def Footer():
    session = [dirFiles("AllBoarders"), dirFiles("Image"), dirFiles("Foot Menu"), dirFiles("CC"),
               dirFiles("FootForm"), dirFiles("Social Media")]
    que_List = list(itertools.product(*session))
    # print(que_List)
    for i in range(0, 50):
        print(i)
        rand = random.randint(1, len(que_List))
        try:
            BannerBorder = Image.open(que_List[rand][0])
            IMG = Image.open(que_List[rand][1])

            FoorMenu = Image.open(que_List[rand][2])
            # FoorMenu.thumbnail((200, 200))

            CC = Image.open(que_List[rand][3])
            CC.thumbnail((200, 200))

            FootForm = Image.open(que_List[rand][4])
            FootForm.thumbnail((400, 400))

            Social = Image.open(que_List[rand][5])
            Social.thumbnail((500, 700))

        except IOError:
            print("Error")

        # Initial the Outer Box
        temp = ImageCons(BannerBorder.size)
        temp.setBase(BannerBorder.size[0], BannerBorder.size[1])
        BannerLayer = BannerBorder.copy()

        # Process IMG
        temp.setTarget(IMG.size[0], IMG.size[1])
        # IMG = scaleByRatio(IMG, temp, 0.6)
        IMG = checkAllRescale(IMG, temp, 8)
        BannerLayer.paste(IMG, findCenterXY(temp.CENTER, temp))

        # Social Media
        temp.setTarget(Social.size[0], Social.size[1])
        # IMG = scaleByRatio(Social, temp, 0.6)
        # Social = checkAllRescale(Social, temp)
        BannerLayer.paste(Social, findCenterXY(temp.RIGHT, temp))

        # FoorMenu
        temp.setTarget(FoorMenu.size[0], FoorMenu.size[1])
        # FoorMenu = checkAllRescale(FoorMenu, temp)
        # FoorMenu = scaleByRatio(FoorMenu, temp, 1.3)
        # BannerLayer.paste(FoorMenu, findCenterXY(temp.RIGHT, temp))
        BannerLayer.paste(FoorMenu, findCenterXY(temp.LEFT, temp))
        # BannerLayer.paste(FoorMenu, findCenterXY(temp.CENTER, temp))
        # BannerLayer.paste(FoorMenu, findCenterXY(temp.RIGHT, temp))

        # CC
        temp.setTarget(CC.size[0], CC.size[1])
        # CC = checkAllRescale(CC, temp)
        # CC = scaleByRatio(CC, temp, 1.3)
        BannerLayer.paste(CC, findCenterXY(temp.BOTTOM_LEFT, temp))

        # FootForm
        temp.setTarget(FootForm.size[0], FootForm.size[1])
        FootForm = checkAllRescale(FootForm, temp, 2)
        # FootForm = scaleByRatio(FootForm, temp, 1.4)
        # BannerLayer.paste(SmallImage, findCenterXY(temp.CENTER, temp))

        BannerLayer.save("Output/Footer/" + str(i) + ".png")


# Text

def Title():
    session = [dirFiles("AllBoarders"), dirFiles("Title")]
    que_List = list(itertools.product(*session))
    # print(que_List)
    for i in range(0, 300):
    # for i in range(0, len(que_List)):
        print(i)
        rand = random.randint(1, len(que_List))
        try:
            BannerBorder = Image.open(que_List[rand][0])
            TEXT = Image.open(que_List[rand][1])
            TEXT.thumbnail((600, 600))
        except IOError:
            print("Error")

        # Initial the Outer Box
        temp = ImageCons(BannerBorder.size)
        temp.setBase(BannerBorder.size[0], BannerBorder.size[1])
        BannerLayer = BannerBorder.copy()

        # Process TEXT
        temp.setTarget(TEXT.size[0], TEXT.size[1])
        # TEXT = scaleByRatio(TEXT, temp)
        # TEXT = checkHeightRescale(TEXT, temp, )
        BannerLayer.paste(TEXT, findCenterXY(temp.RIGHT, temp))
        BannerLayer.save("Output/Title/" + str(i) + ".png")



# Text

def Paragraph():
    session = [dirFiles("AllBoarders"), dirFiles("Title"), dirFiles("Paragraph")]
    que_List = list(itertools.product(*session))
    # print(que_List)
    for i in range(0, 300):
    # for i in range(0, len(que_List)):
        print(i)
        rand = random.randint(1, len(que_List))
        try:
            BannerBorder = Image.open(que_List[rand][0])
            TEXT = Image.open(que_List[rand][2])
            TEXT.thumbnail((600, 600))
            TITLE = Image.open(que_List[rand][1])
            TITLE.thumbnail((600, 600))
        except IOError:
            print("Error")

        # Initial the Outer Box
        temp = ImageCons(BannerBorder.size)
        temp.setBase(BannerBorder.size[0], BannerBorder.size[1])
        BannerLayer = BannerBorder.copy()

        # Process TEXT
        temp.setTarget(TEXT.size[0], TEXT.size[1])
        # TEXT = scaleByRatio(TEXT, temp)
        TEXT = checkAllRescale(TEXT, temp)
        TEXT = scaleByRatio(TEXT, temp, 1.8)
        # TEXT = checkHeightRescale(TEXT, temp, )
        BannerLayer.paste(TEXT, findCenterXY(temp.CENTER, temp))
        BannerLayer.paste(TEXT, findCenterXY(temp.LEFT, temp))
        BannerLayer.paste(TEXT, findCenterXY(temp.RIGHT, temp))

        # Process Title
        temp.setTarget(TITLE.size[0], TITLE.size[1])
        # TEXT = scaleByRatio(TITLE, temp)

        # TITLE = checkAllRescale(TITLE, temp)
        # TEXT = checkHeightRescale(TITLE, temp, )
        BannerLayer.paste(TITLE, findCenterXY(temp.TOP_LEFT, temp))


        BannerLayer.save("Output/Paragraph/" + str(i) + ".png")

# Paragraph()
# Title()
# Footer()
# header()
# imageFlip()
# plainImageGallary()
# structRightImageBox()
# structLeftImageBox()
# structCenterImageBox()
