import re
import markdown
from bs4 import BeautifulSoup
from homepagebuilder.interfaces import script, require
from homepagebuilder.core.utils.encode import encode_escape
from homepagebuilder.core.utils.event import set_triggers, listen_event

parsers_module = require('markdown_parsers')
create_node= parsers_module.create_node
markdown_process_pipeline = []

DEL_PATTERN = re.compile(r'~~(.*)~~')

def markdown_processor(func):
    '''markdown 额外处理函数装饰器'''
    markdown_process_pipeline.append(func)
    return func

def html2xaml(html,context):
    '''html转为xaml代码'''
    soup = BeautifulSoup(html,'html.parser')
    xaml = ''
    for tag in soup.find_all(recursive=False):
        xaml += create_node(tag,context,[]).convert()
    return xaml

DELETE_PATTEN = re.compile(r'~~(.*)~~')
BLOCK_CODE_PATTEN = re.compile(r'`{3,}\s*(\S*)\s*\n(.*?)\n`{3,}', flags=re.RegexFlag.DOTALL)

@markdown_processor
def md_del_replace(md:str):
    '''转译删除线'''
    return re.sub(DELETE_PATTEN, r'<del>\1</del>',md)

@markdown_processor
def block_code_replace(md:str):
    '''转译块状代码'''
    def repl(matchobj:re.Match) -> str:
        # 注意：bs4 会将转义字符先反转义一次
        return f'<blockcode lang="{matchobj.group(1).upper()}" code="{encode_escape(matchobj.group(2), with_special=True)}"/>'
    return re.sub(BLOCK_CODE_PATTEN, repl, md)

def convert(md,context):
    '''生成xaml代码'''
    for processor in markdown_process_pipeline:
        md = processor(md)
    html = markdown.markdown(md)
    xaml = html2xaml(html,context)
    return xaml

@script('MarkdownPresenter')
def markdown_presenter(card,context,**_):
    '''从markdown生成xaml代码脚本'''
    md = card['markdown']   
    return convert(md,context)
