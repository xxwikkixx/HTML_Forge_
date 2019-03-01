import itertools
import random
from PIL import Image

from ImageDatasetCreation import checkAllRescale, findCenterXY, ImageCons, dirFiles


def structLeftImageBox():
    session = [dirFiles("OuterBox"), dirFiles("Image"), dirFiles("Text")]
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
    session = [dirFiles("OuterBox"), dirFiles("Image"), dirFiles("Text")]
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
    session = [dirFiles("OuterBox"), dirFiles("Image"), dirFiles("Text")]
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



# structCenterImageBox()
# structLeftImageBox()
