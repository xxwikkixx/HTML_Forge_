# AI detected user attributes, actual code

attributesDB = {
    # This we are going to user stock image
    # "herf": "herf=",
    # "src": "src=",
    # "alt": "alt=",

    "w": "width=",
    "h": "height=",
    "align": "align=",

}

# AI Detected Tag, actual code
blockTypeTagsDB = {
    "button": "<button >",
    "image": "<img >",
    "textInput": "<input >",

    "password": "<input type=\"password\">",

    "textArea": "<textArea >",
    "radioButton": "<input type= \"radio\">",
    "checkbox": "<input type= \"checkbox\">",

    "dropdown": "<select name= \"dropdown\"> " +
                "<option value = \"option1\"> option1 </option>" +
                "<option value = \"option2\"> option2 </option>" +
                "<option value = \"option3\"> option3 </option>",

    "table": "<table >",
    "row": "<tr >",
    "col": "<td >",

    "paragraph": "<p >",
    "H1": "<h1 >",
    "H2": "<h2 >",
    "H3": "<h3 >",
    "H4": "<h4 >",
    "H5": "<h5 >",
    "H6": "<h6 >",
    "b": "<b >",
    "i": "<i >",

    "orderedLists": "<ol >",
    "unorderedLists": "<ul >",
    "listItems": "<li >",
r
    "nav": "<nav >" +
            "<a href=> Page1 </a>" +
            "<a href=> Page2 </a>"
}


def objectToBlockCode(blockType, listOfAttributes, inHTML):
    # iterate the whole list and append to String
    HTML = blockTypeTagsDB[blockType]
    strBuilder = ""

    for char in HTML:
        if char == ">":
            break
        else:
            strBuilder += char

    for key, value in listOfAttributes.items():
        attrStrbuilder = str(attributesDB[key])
        if str(value).isalpha():
            attrStrbuilder += "\"" + str(value) + "\""
        else:
            attrStrbuilder += str(value)
        attrStrbuilder += " "
        strBuilder += attrStrbuilder

    strBuilder += ">"
    strBuilder += inHTML
    strBuilder += getEndTag(blockType)

    return strBuilder


def getEndTag(blockType):
    HTML = blockTypeTagsDB[blockType]
    strBuilder = ""

    for char in HTML:
        if char == " ":
            break

        if char == ">":
            break

        elif char != "<":
            strBuilder += char

    return "</" + strBuilder + ">"


def runExample():
    print(getEndTag("radioButton"))
    print(getEndTag("paragraph"))
    print(getEndTag("password"))
    print("\n\n")
    listOfAttrFromSingleBlock = {"w": 250, "h": 100, "align": "center"}
    print(objectToBlockCode("image", listOfAttrFromSingleBlock, "this is in HTML Text"))

runExample()
