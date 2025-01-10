import re
import markdown
from bs4 import BeautifulSoup
from homepagebuilder.interfaces import script, require
from homepagebuilder.core.utils.event import set_triggers, listen_event

parsers_module = require('markdown_parsers')
create_node= parsers_module.create_node
markdown_process_pipeline = []

DEL_PATTERN = re.compile(r'~~(.*)~~')

def markdown_processor(func):
    '''markdown 额外处理函数装饰器'''
    markdown_process_pipeline.append(func)
    return func

@markdown_processor
def md_del_replace(md:str):
    '''转译删除线'''
    return re.sub(DEL_PATTERN ,r'<del>\1</del>',md)

def html2xaml(html,context):
    '''html转为xaml代码'''
    soup = BeautifulSoup(html,'html.parser')
    xaml = ''
    for tag in soup.find_all(recursive=False):
        xaml += create_node(tag,context,[]).convert()
    return xaml

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
