import os
from shutil import copyfile
from SessionIDGen import generateSessionID, generateID


class ImageProcessSession:
    def createSessionDir(self):
        cwd = os.getcwd()
        print (cwd)
        self.sessionPath = cwd+"/UserUpload/" + self.sessionID + "/"
        os.mkdir(self.sessionPath)

    def createCropDir(self):
        self.cropDir = self.sessionPath + "ImageCrops" + "/"
        os.mkdir(self.cropDir)

    def createDebugDir(self):
        self.debugDir = self.sessionPath + "Debug" + "/"
        os.mkdir(self.debugDir)

    def __init__(self):
        self.sessionID = generateSessionID()
        self.sessionID = generateID()
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
        return self.sessionPath + "/" + self.fileName

    def userImageImport(self, src):
        folderPath = (os.getcwd())
        print (src)
        baseName = os.path.basename(src)
        self.fileName = baseName
        copyfile(src, self.sessionPath + baseName)




