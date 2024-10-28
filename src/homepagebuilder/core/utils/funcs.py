from typing import Dict
def transform(original_dict:Dict):
    newdict = {}
    for k,v in original_dict.items():
        newdict[v] = k
    return newdict