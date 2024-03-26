from Core.FileIO import regist_fileread_function,readString
import re

def readMarkdown(filepath:str):
    string = readString(filepath=filepath)
    string, card = sep_attr(string)
    card['markdown'] = string
    return card

ATTR_PATTERN = re.compile(r'^\-{3,}\n((.*\n)+)\-{3,}\n')
def sep_attr(md):
    attr = {}
    matchs = re.match(ATTR_PATTERN, md)
    if matchs:
        for attr_str in matchs.groups()[0].split('\n'):
            if ':' not in attr_str:
                continue
            attr_name,attr_value = attr_str.split(':',1)
            attr_name = attr_name.replace(' ','')
            attr_value = attr_value.removeprefix(' ')
            attr_value = attr_value.removesuffix(' ')
            attr[attr_name] = attr_value
    md = re.sub(ATTR_PATTERN, '', md)
    return md,attr

regist_fileread_function(readMarkdown,['md','markdown'])