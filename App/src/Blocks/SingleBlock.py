class SingleBlock():
    def __init__(self):
        self.blockID = 0
        self.blockType = 0

        self.attributesDict = {}
        self.behaviorsDict = {}

        self.inHTML = ""
        self.blockCode = ""

        self.x_Location = 0
        self.y_Location = 0
        self.width = 0
        self.height = 0

        self.image_path = ""

    def setBlockID(self, assignID: int):
        self.blockID = assignID

    def getBlockID(self):
        return self.blockID

    def setBlockType(self, blockType: int):
        self.blockType = blockType

    def getBlockType(self):
        return self.blockType

    # Attribute and Behavior Dictionary Getter and Setters
    def appendAttribute(self, attributeTag: int, userSetProperty: str):
        self.attributesDict[attributeTag] = userSetProperty

    def removeAttribute(self, attributeTag: int):
        del self.attributesDict[attributeTag]

    def getBlockAttributes(self):
        return self.attributesDict

    def appendBehavior(self, behaviorTag: int, userSetProperty: str):
        self.behaviorsDict[behaviorTag] = userSetProperty

    def removeBehavior(self, behaviorTag: int):
        del self.behaviorDict[behaviorTag]

    def getBlockBehavior(self):
        return self.behaviorsDict

    # HTML of each individual building Block Objects
    def setSingleBlock_HTMLCode(self, HTMLcode: str):
        self.blockCode = HTMLcode

    def getSingleBlock_HTMLCode(self):
        return self.blockCode

    def setSingleBlock_InHTML(self, userText: str):
        self.inHTML = userText

    def getSingleBlock_InHTML(self):
        return self.inHTML

    def setX_Location(self, xVal: int):
        self.x_Location = xVal

    def getX_Location(self):
        return self.x_Location

    def setY_Location(self, yVal: int):
        self.y_Location = yVal

    def getY_Location(self):
        return self.y_Location


    def set_Width(self, wVal: int):
        self.width = wVal

    def get_Width(self):
        return self.width

    def set_Height(self, hVal:int):
        self.height= hVal

    def get_Height(self):
        return self.height

    def setImagePath(self, path: str):
        self.image_path = path

    def getImagePath(self):
        return self.image_path
