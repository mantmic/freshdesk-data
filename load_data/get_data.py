import json

def loadFileData(filename):
    file = open(filename, 'r')
    return(json.load(file))
