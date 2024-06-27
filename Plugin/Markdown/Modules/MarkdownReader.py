'''
Markdown 读取模块
'''
import re
import ast
from Interfaces import file_reader, read_string

# 提取列表项：(?:\[?\s*)(\".*?\"|\'.*?\'|[^,]*?)(?:\s*[,|\]])

@file_reader(['md','markdown'])
def read_markdown(filepath:str):
    '''读取markdown文件方法'''
    string = read_string(filepath=filepath)
    string, card = sep_attr(string)
    card['markdown'] = replace_with_wiki_link(string)
    return card

WIKILINK_APTTERN  = re.compile(r'\[\[(.*?)\]\]')
def replace_with_wiki_link(text):
    '''替换 MCW 链接'''
    replaced_text = re.sub(WIKILINK_APTTERN , r'[\1](https://zh.minecraft.wiki/w/\1)', text)
    return replaced_text

ATTR_PATTERN = re.compile(r'^\-{3,}\n((?:.*\n)+)\-{3,}(?:\n|$)')
def sep_attr(md):
    '''分离markdwon正文与文档属性'''
    attr = {}
    matchs = re.match(ATTR_PATTERN, md)
    if matchs:
        for attr_str in matchs.groups()[0].split('\n'):
            if attr_str.startswith('#'):
                continue
            if ':' not in attr_str:
                continue
            attr_name,attr_value = attr_str.split(':',1)
            attr_name = attr_name.replace(' ','')
            attr_value = attr_value.removeprefix(' ')
            attr_value = attr_value.removesuffix(' ')
            if attr_value.startswith('[') and attr_value.endswith(']'):
                attr_value = ast.literal_eval(attr_value)
            attr[attr_name] = attr_value
    md = re.sub(ATTR_PATTERN, '', md)
    return md,attr
