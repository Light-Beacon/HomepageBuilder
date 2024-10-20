import os
from Builder.Core.IO import Dire

dn = os.path.dirname

ENV_PATH = dn(dn(dn(dn(__file__))))


def getbuilderpath(path:str):
    path = path.replace('/',os.sep)
    return ENV_PATH + os.sep + path

def getbuilderdire(path:str):
    return Dire(getbuilderpath(path))