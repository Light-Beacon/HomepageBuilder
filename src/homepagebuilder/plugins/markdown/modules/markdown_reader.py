'''
Markdown 读取模块
'''
import re
from typing import TYPE_CHECKING
import yaml
from homepagebuilder.interfaces import file_reader, read_string

if TYPE_CHECKING:
    from pathlib import Path

# 提取列表项：(?:\[?\s*)(\".*?\"|\'.*?\'|[^,]*?)(?:\s*[,|\]])

@file_reader('md', 'markdown')
def read_markdown(filepath:'Path'):
    '''读取markdown文件方法'''
    string = read_string(filepath=filepath)
    string, card = sep_attr(string)
    card['markdown'] = string
    return card

ATTR_PATTERN = re.compile(r'^\-{3,}\n((?:.*\n)+?)\-{3,}(?:\n|$)')
def sep_attr(md):
    '''分离markdwon正文与文档属性'''
    attr = {}
    matchs = re.match(ATTR_PATTERN, md)
    if matchs:
        attr = yaml.safe_load(matchs.groups()[0])
    md = re.sub(ATTR_PATTERN, '', md)
    return md,attr
