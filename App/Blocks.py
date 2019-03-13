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

    def JSONFormat(self, path):
        """
        Generate json format file with given export path.
        :param path: string  Path to exporting JSON file
        """
        data = {}
        for i in self.blocks:
            data[i] = {'ID': self.getBlockByID(i).getBlockID(),
                       'X_Axis': self.getBlockByID(i).getX_Location(),
                       'Y_Axis': self.getBlockByID(i).getY_Location(),
                       'Width': self.getBlockByID(i).get_Width(),
                       'Height': self.getBlockByID(i).get_Height(),
                       'Predictions': self.getBlockByID(i).getPrediction(),
                       'Best_Predictions': self.getBlockByID(i).getBestPrediction(),
                       'Second_Best': self.getBlockByID(i).getScondBest(),
                       'Image_Crop_Path': self.getBlockByID(i).getImagePath(),
                       'Block_Code': self.getBlockByID(i).getSingleBlock_HTMLCode()}

        with open(path, 'w') as outfile:
            json.dump(data, outfile, indent=3, sort_keys=False)
