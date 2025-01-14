import re
import markdown
from bs4 import BeautifulSoup
from homepagebuilder.interfaces import script, require
from homepagebuilder.core.utils.encode import encode_escape

parsers_module = require('markdown_parsers')
create_node= parsers_module.create_node

def html2xaml(html,context):
    '''html转为xaml代码'''
    soup = BeautifulSoup(html,'html.parser')
    xaml = ''
    for tag in soup.find_all(recursive=False):
        xaml += create_node(tag,context,[]).convert()
    return xaml

DELETE_PATTEN = re.compile(r'~~(.*)~~')
BLOCK_CODE_PATTEN = re.compile(r'`{3,}\s*(\S*)\s*\n(.*?)\n`{3,}', flags=re.RegexFlag.DOTALL)

def md_del_replace(md:str):
    '''转译删除线'''
    return re.sub(DELETE_PATTEN, r'<del>\1</del>',md)

def block_code_replace(md:str):
    '''转译块状代码'''
    def repl(matchobj:re.Match) -> str:
        # 注意：bs4 会将转义字符先反转义一次
        return f'<blockcode lang="{matchobj.group(1).upper()}" code="{encode_escape(matchobj.group(2), with_special=True)}"/>'
    return re.sub(BLOCK_CODE_PATTEN, repl, md)

def convert(card,context):
    '''生成xaml代码'''
    md = card['markdown']
    md = md_del_replace(md)
    md = block_code_replace(md)
    html = markdown.markdown(md)
    xaml = html2xaml(html,context)
    return xaml

@script('MarkdownPresenter')
def markdown_presenter(card,context,**_):
    '''从markdown生成xaml代码脚本'''
    return convert(card,context)
