from random import randint
import logging
import datetime

def generateID():
    pas = ''
    digCounter = 0
    for j in range(0, 25):
        if digCounter != 0 and digCounter % 5 == 0:
            pas += '_'
        numAndAlp = randint(0, 2)
        if numAndAlp == 1:
            pas += (chr(randint(48, 57)))  # Number Generate
        elif numAndAlp == 0:
            pas += (chr(randint(65, 90)))  # Upper Case
        else:
            pas += (chr(randint(97, 112)))  # Lower Case
        digCounter += 1
    logging.debug(pas)
    return pas


def generateSessionID():
    x = datetime.datetime.now()
    return str(x.strftime("%y_%m_%dd_%Hh_%Mm%f"))
    
# def main():
#     lisense = []
    # logging.basicConfig(filename='123.txt', level=logging.DEBUG, format='%(asctime)s- %(levelname)s- %(message)s')
    # amounts = int(input('Please input how many SERIAL LISENSE NUMBER you want to generate: '))
    # for i in range(0, 1):
    #     lisense.append(generateID())
    #

    # print(generateSessionID())
    # x = datetime.datetime.now()
    # print(x.strftime("%Yyr_%mmo_%dd_%Hh_%Mm_%Ss_%fms"))
    # print(lisense)


# if __name__ == "__main__":
    # main()
