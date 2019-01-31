from SingleBlock import SingleBlock

blocks = {}

IDAssignCount = 1

# Function will return individual block as an SingleBlock Object
def getBlockByID(blockID: int):
    return blocks[blockID]


def getTotalBlocks():
    return len(blocks)


def addBlock():
    global IDAssignCount
    blocks[IDAssignCount] = SingleBlock()
    getBlockByID(IDAssignCount).setBlockID(IDAssignCount)
    IDAssignCount += 1


# Example of how to use this
def runExample():
    addBlock()  # Creates a new single block object and assigned with ID 1
    addBlock()  # Block ID 2
    addBlock()
    addBlock()
    addBlock()

    # Example 1
    print(blocks, "\n")
    getBlockByID(1).appendAttribute(1, "green")
    getBlockByID(1).appendAttribute(2, "24px")
    print("Block attributes of block", getBlockByID(1).getBlockID(), "is: ", getBlockByID(1).getBlockAttributes())

    # Example 2
    getBlockByID(2).setSingleBlock_InHTML("This is a Button")
    getBlockByID(2).setSingleBlock_HTMLCode("<button>" + getBlockByID(2).getSingleBlock_InHTML() + "</button>")
    print("block 2 HTML code: ", getBlockByID(2).getSingleBlock_HTMLCode())


runExample()
