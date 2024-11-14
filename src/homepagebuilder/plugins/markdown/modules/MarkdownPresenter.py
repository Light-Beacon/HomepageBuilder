import re
import markdown
from bs4 import BeautifulSoup
from homepagebuilder.interfaces import script, require

parsers_module = require('markdown_parsers')
create_node= parsers_module.create_node

def html2xaml(html,env):
    '''html转为xaml代码'''
    soup = BeautifulSoup(html,'html.parser')
    xaml = ''
    for tag in soup.find_all(recursive=False):
        xaml += create_node(tag,env,[]).convert()
    return xaml

del_pattern = re.compile(r'~~(.*)~~')

def md_del_replace(md:str):
    '''转译删除线'''
    return re.sub(del_pattern,r'<del>\1</del>',md)

def convert(card,env):
    '''生成xaml代码'''
    md = card['markdown']
    md = md_del_replace(md)
    html = markdown.markdown(md)
    xaml = html2xaml(html,env)
    return xaml

@script('MarkdownPresenter')
def script(card,env,**_):
    '''从markdown生成xaml代码脚本'''
    return convert(card,env)
