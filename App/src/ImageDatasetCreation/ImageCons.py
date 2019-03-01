class ImageCons:
    def __init__(self, size):
        self.TARGET_H = 0
        self.TARGET_W = 0

        print(size)
        self.BASE_IMAGE_WIDTH = size[0]
        self.BASE_IMAGE_HEIGHT = size[1]

        self.TOP_LEFT = int(size[0] / 4 * 1), int(size[1] / 4 * 1)
        self.LEFT = int(size[0] / 4 * 1), int(size[1] / 4 * 2)
        self.BOTTOM_LEFT = int(size[0] / 4 * 1), int(size[1] / 4 * 3)
        self.CENTER = int(size[0] / 4 * 2), int(size[1] / 4 * 2)
        self.CENTER_BOTTOM = int(size[0] / 4 * 2), int(size[1] / 4 * 3)
        self.TOP_RIGHT = int(size[0] / 4 * 3), int(size[1] / 4 * 1)
        self.RIGHT = int(size[0] / 4 * 3), int(size[1] / 4 * 2)
        self.BOTTOM_RIGHT = int(size[0] / 4 * 3), int(size[1] / 4 * 3)
        self.CENTER_TOP = int(size[0] / 4 * 2), int(size[1] / 4 * 1)

    def setCorners(self, BASE_IMAGE_WIDTH, BASE_IMAGE_HEIGHT):
        self.BASE_IMAGE_WIDTH = BASE_IMAGE_WIDTH
        self.BASE_IMAGE_HEIGHT = BASE_IMAGE_HEIGHT

    def setTarget(self, w, h):
        self.TARGET_W = w
        self.TARGET_H = h

    def setBase(self, w, h):
        self.BASE_IMAGE_HEIGHT = h
        self.BASE_IMAGE_WIDTH = w

    def getT_W(self):
        return self.TARGET_W

    def getT_H(self):
        return self.TARGET_H

    def getB_W(self):
        return self.BASE_IMAGE_WIDTH

    def getB_H(self):
        return self.BASE_IMAGE_HEIGHT
