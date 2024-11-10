import os

dn = os.path.dirname

ENV_PATH = dn(dn(dn(__file__)))

def fmtpath(*paths) -> str:
    result = ''
    for path in paths:
        result += path.replace('/',os.sep)
    return result

def getbuilderpath(path:str):
    path = fmtpath(path)
    return ENV_PATH + os.sep + path