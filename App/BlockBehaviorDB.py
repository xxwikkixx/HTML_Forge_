# from src.Blocks import Blocks
# from src.Blocks import SingleBlock

#
# blockBehaviorDB = {
#     1: "Menu",
#     2: "parallax",
# }

# File for testing purposes

import os
import json

usersession = 'J6Pmj_1C4Gl_oimd4_2Faof_NK5J0'

def jsonFile():
    dirc = os.path.dirname(os.path.realpath(__file__))
    projectStruct = 'Assets'
    fullPath = os.path.join(dirc, projectStruct)

    userUploadPath = os.path.join(dirc, "UserUpload")
    jsonPath = os.path.join(userUploadPath, usersession)
    print(jsonPath)

def moifyJson():
    dirc = os.path.dirname(os.path.realpath(__file__))
    userUploadPath = os.path.join(dirc, "UserUpload")
    jsonPath = os.path.join(userUploadPath, usersession)

    dict = []

    with open(os.path.join(jsonPath, 'data.json'), 'r') as f:
        jsonData = json.load(f)
        jsData = jsonData["blocks"]
        for i in jsData:
            resp = i["Image_Crop_Path"]
            for pths in resp:
                pass
            print(resp)


moifyJson()