import os
from shutil import copyfile
from ImageProcessing.SessionIDGen import generateSessionID


class ImageProcessSession:
    def createSessionDir(self):
        self.sessionPath = "UserUpload/" + self.sessionID + "/"
        os.mkdir(self.sessionPath)

    def createCropDir(self):
        self.cropDir = self.sessionPath + "/ImageCrops" + "/"
        os.mkdir(self.cropDir)

    def createDebugDir(self):
        self.debugDir = self.sessionPath + "/Debug" + "/"
        os.mkdir(self.debugDir)

    def __init__(self):
        self.sessionID = generateSessionID()
        self.sessionPath = ""
        self.cropDir = ""
        self.debugDir = ""
        self.fileName = ""

        self.createSessionDir()
        self.createCropDir()
        self.createDebugDir()

    def getSessionID(self):
        return self.sessionID

    def getSessionPath(self):
        return self.sessionPath

    def setSessionPath(self, newSrc):
        self.sessionPath = newSrc

    def getCropDir(self):
        return self.cropDir

    def getDebugDir(self):
        return self.debugDir

    def getpathToUserImage(self):
        folderPath = (os.getcwd())
        return folderPath + "/" + self.sessionPath + "/" + self.fileName

    def userImageImport(self, src):
        folderPath = (os.getcwd())
        baseName = os.path.basename(src)
        self.fileName = baseName
        copyfile(src, folderPath + "/" + self.sessionPath + baseName)




