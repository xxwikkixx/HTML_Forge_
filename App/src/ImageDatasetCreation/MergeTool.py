import os
import random

from PIL import Image

TARGET_WIDTH = 0
TARGET_HEIGHT = 0


def getRandom():
    RANDOM_SHIFT_PIXAL = 10
    plusnegative = random.randint(0, 1)
    if plusnegative == 1:
        return random.randint(1, RANDOM_SHIFT_PIXAL)
    else:
        return -random.randint(1, RANDOM_SHIFT_PIXAL)


def dirFiles(itemType):
    path = "Assets/" + itemType
    lst = []
    for item in os.listdir(path):
        if not item.startswith('.') and os.path.isfile(os.path.join(path, item)):
            lst.append(item)

    # lst = os.listdir(path)
    for i in range(0, len(lst)):
        temp = lst[i]
        lst[i] = path + "/" + temp
    return lst


def findCenterXY(snapCorner, base):
    # print(base.getT_H())
    # print(int(snapCorner[0] - base.getT_W() / 2), int(snapCorner[1] - base.getT_H() / 2))
    return int(snapCorner[0] - base.getT_W() / 2), int(snapCorner[1] - base.getT_H() / 2)


def checkAllRescale(img, base , scaleby=6):
    width_thres = int(base.getB_W() / scaleby)
    height_thres = int(base.getB_H() / scaleby)
    if img.size[0] > width_thres or img.size[1] > height_thres:
        wpercent = (width_thres / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((width_thres, hsize), Image.ANTIALIAS)
        base.setTarget(width_thres, hsize)
        return img




def checkHeightRescale(img, base):
    width_thres = int(base.getB_W() / 5)
    height_thres = int(base.getB_H() / 5)
    if img.size[1] > height_thres:
        wpercent = (width_thres / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((width_thres, hsize), Image.ANTIALIAS)
        base.setTarget(width_thres, hsize)
        return img


def checkWidthRescale(img, base):
    width_thres = int(base.getB_W() / 5)
    height_thres = int(base.getB_H() / 5)
    if img.size[0] > width_thres:
        wpercent = (width_thres / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((width_thres, hsize), Image.ANTIALIAS)
        base.setTarget(width_thres, hsize)
        return img


def scaleByRatio(img, base, ratio):
    img = img.resize((int(int(img.size[0]) * ratio), int(int(img.size[1]) * ratio)), Image.ANTIALIAS)
    base.setTarget(int(int(img.size[0]) * ratio), int(int(img.size[1]) * ratio))
    return img


