class SingleBlock:
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

        self.prediction = []
        self.bestPrediction = []
        self.secondBestPrediction = []

        # self.predictionScore = []

    def setPrediction(self, prediction):
        self.prediction = prediction
        self.bestPrediction = max(prediction, key=lambda x: x[1])
        arr = sorted(prediction, key=lambda x: x[1])
        self.secondBestPrediction = arr[len(arr)-2]
        # self.predictionScore = score

    def getPrediction(self):
        return self.prediction

    def getBestPrediction(self):
        return self.bestPrediction

    def setBestPrediction(self, lst):
        self.bestPrediction = lst

    def getScondBest(self):
        return self.secondBestPrediction

    def setBlockID(self, assignID):
        self.blockID = assignID

    def getBlockID(self):
        return self.blockID

    def setBlockType(self, blockType):
        self.blockType = blockType

    def getBlockType(self):
        return self.blockType

    # Attribute and Behavior Dictionary Getter and Setters
    def appendAttribute(self, attributeTag, userSetProperty):
        self.attributesDict[attributeTag] = userSetProperty

    def removeAttribute(self, attributeTag):
        del self.attributesDict[attributeTag]

    def getBlockAttributes(self):
        return self.attributesDict

    def appendBehavior(self, behaviorTag, userSetProperty):
        self.behaviorsDict[behaviorTag] = userSetProperty

    def removeBehavior(self, behaviorTag):
        del self.behaviorDict[behaviorTag]

    def getBlockBehavior(self):
        return self.behaviorsDict

    # HTML of each individual building Block Objects
    def setSingleBlock_HTMLCode(self, HTMLcode):
        self.blockCode = HTMLcode

    def getSingleBlock_HTMLCode(self):
        return self.blockCode

    def setSingleBlock_InHTML(self, userText):
        self.inHTML = userText

    def getSingleBlock_InHTML(self):
        return self.inHTML

    def setX_Location(self, xVal):
        self.x_Location = xVal

    def getX_Location(self):
        return self.x_Location

    def setY_Location(self, yVal):
        self.y_Location = yVal

    def getY_Location(self):
        return self.y_Location

    def set_Width(self, wVal):
        self.width = wVal

    def get_Width(self):
        return self.width

    def set_Height(self, hVal):
        self.height = hVal

    def get_Height(self):
        return self.height

    def setImagePath(self, path):
        self.image_path = str(path)

    def getImagePath(self):
        return self.image_path