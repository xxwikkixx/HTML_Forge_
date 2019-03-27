from SingleBlock import SingleBlock
import json


class Blocks:
    """
    Class that use for storing all the single block class instances
    """

    def __init__(self):
        """
            Class initialization. with variable of list of blocks
            :param
                self : self
            :var
                blocks : list Contains all the singleBlock class instances
                IDAssignCount : ID Assign counter
        """
        self.blocks = {}
        self.IDAssignCount = 1

    def getBlockByID(self, blockID):
        """
            Getter for singleblock that stored in blocks, and search base on given block ID
            :param
                self: self
                blockID: int  The ID that assigned to each singleBlock during initialization
            :return
                singleBlock: object singleBlock class object
        """
        return self.blocks[blockID]

    def addBlock(self):
        """
            initialize, add new single block class to the list
            :param
                self: self
        """
        # self.IDAssignCount
        self.blocks[self.IDAssignCount] = SingleBlock()
        self.getBlockByID(self.IDAssignCount).setBlockID(self.IDAssignCount)
        self.IDAssignCount += 1

    def JSONFormat(self, path, sessionID):
        """
        Generate json format file with given export path.
        :param path: string  Path to exporting JSON file
        """
        HOST_PATH = "htmlforge-dev.us-east-1.elasticbeanstalk.com"
        data = {}
        temp = []
        for i in self.blocks:
            temp.append({'ID': self.getBlockByID(i).getBlockID(),
                         'X_Axis': self.getBlockByID(i).getX_Location(),
                         'Y_Axis': self.getBlockByID(i).getY_Location(),
                         'Width': self.getBlockByID(i).get_Width(),
                         'Height': self.getBlockByID(i).get_Height(),
                         'Predictions': self.getBlockByID(i).getPrediction(),
                         'Best_Predictions': self.getBlockByID(i).getBestPrediction(),
                         'Second_Best': self.getBlockByID(i).getScondBest(),
                         'Image_Crop_Path': "http://" + HOST_PATH + "/api/blocksdetected/"+sessionID+"/CropImage/"+str(self.getBlockByID(i).getBlockID()),
                         'Server_Local_Image_Path': self.getBlockByID(i).getImagePath(),
                         'Block_Code': self.getBlockByID(i).getSingleBlock_HTMLCode()})
        # /api/blocksdetected/<usersession>/CropImage/<filename>
        # /api/blocksdetected/getDebugImage/<usersession>
        data["debugImage"] = HOST_PATH + "/api/blocksdetected/getDebugImage/" + str(sessionID)
        data["blocks"] = temp
        # print(data)
        with open(path, 'w') as outfile:
            json.dump(data, outfile, indent=3, sort_keys=False)

    def changePath(self, sessionID):
        for i in range(1, len(self.blocks)):
            # self.getBlockByID(i).setImagePath(i + "png")
            # print(self.getBlockByID(i).getImagePath())
            self.getBlockByID(i).setImagePath("http://localhost:63342/App/UserUpload/" + sessionID + "/ImageCrops/" + str(i) + ".png")
