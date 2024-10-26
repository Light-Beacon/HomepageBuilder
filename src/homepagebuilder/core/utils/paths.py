import os

dn = os.path.dirname

ENV_PATH = dn(dn(dn(__file__)))

def getpath(path:str) -> str:
    return path.replace('/',os.sep)

def getbuilderpath(path:str):
    path = getpath(path)
    return ENV_PATH + os.sep + path