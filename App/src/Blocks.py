from SingleBlock import SingleBlock
import json

class Blocks:
    def __init__(self):
        self.blocks = {}
        self.IDAssignCount = 1

    # Function will return individual block as an SingleBlock Object
    def getBlockByID(self, blockID):
        return self.blocks[blockID]

    def getTotalBlocks(self):
        return len(self.blocks)

    def addBlock(self):
        # self.IDAssignCount
        self.blocks[self.IDAssignCount] = SingleBlock()
        self.getBlockByID(self.IDAssignCount).setBlockID(self.IDAssignCount)
        self.IDAssignCount += 1

    def JSONFormat(self, path):
        data = {}
        for i in self.blocks:
            data[i] = {'ID': self.getBlockByID(i).getBlockID(),
                       'X_Axis': self.getBlockByID(i).getX_Location(),
                       'Y_Axis': self.getBlockByID(i).getY_Location(),
                       'Width': self.getBlockByID(i).get_Width(),
                       'Height': self.getBlockByID(i).get_Height(),
                       'Predictions': self.getBlockByID(i).getPrediction(),
                       'Best_Predictions': self.getBlockByID(i).getBestPrediction(),
                       'Image_Crop_Path': self.getBlockByID(i).getImagePath(),
                       'Block_Code': self.getBlockByID(i).getSingleBlock_HTMLCode()}

        with open(path, 'w') as outfile:
            json.dump(data, outfile, indent=3)
