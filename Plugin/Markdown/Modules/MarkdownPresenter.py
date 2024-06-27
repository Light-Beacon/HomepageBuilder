import re
import markdown
from bs4 import BeautifulSoup
from Interfaces import script,encode_escape,Logger

logger = Logger('MarkdownPresenter')

def get_replacement(name:str,attrs:dict):
    '''获取替换的字符串'''
    component_name = name
    replace_list = []
    if name == 'h1':
        return (None,None)
    if name[0] == 'h' and name[1:].isdigit():
        component_name = 'h'
        replace_list.append(('level',name[1:]))
    elif name == 'a':
        replace_list.append(('link',attrs['href']))
    elif name == 'img':
        replace_list.append(('source',attrs['src']))
        if len(attrs['alt']) > 0:
            component_name = 'titled-img'
            replace_list.append(('alt',attrs['alt']))
    return (component_name, replace_list)

def get_element_frame(name,attrs,res):
    '''获取元素框架'''
    components:dict[str,str] = res.components
    component_name, replace_list = get_replacement(name,attrs)
    if not component_name: # e.g H1
        return ''
    replace_str = components.get(component_name)
    if replace_str is None:
        logger.warning(f'markdown 中存在尚不支持的元素{name}')
        return None
    for k,v in replace_list:
        replace_str = replace_str.replace(f'${{{k}}}',encode_escape(v))
    return replace_str

FIRSTLINE_SPACES = '    '
LINE_BREAK = '<LineBreak/>'
INLINE_ELEMENTS = ['li','p','em','strong','a','code','del']

def is_inline(tag):
    '''判断标签是否是行内元素'''
    if isinstance(tag,str):
        return True
    return tag.name in INLINE_ELEMENTS

def list_item2xaml(tag,res):
    '''列表元素转为xaml代码'''
    if tag.name != 'li':
        raise ValueError()
    element_frame:str = get_element_frame(tag.name,{},res)
    if element_frame is None:
        return str(tag)
    content = ''
    in_paragraph = False
    if tag.contents:
        for child in tag.contents:
            if is_inline(child):
                if child == '\n':
                    continue
                if not in_paragraph:
                    content += '<Paragraph>'
                    in_paragraph = True
                if isinstance(child,str):
                    content += encode_escape(child)
                else:
                    content += element2xaml_general(child,res)
            else:
                if in_paragraph:
                    content += '</Paragraph>'
                    in_paragraph = False
                content += element2xaml_general(child,res)
        if in_paragraph:
            content += '</Paragraph>'
    return element_frame.replace('${content}',content)

def quote2xaml(tag,res):
    '''引文元素转为xaml代码'''
    if tag.name != 'blockquote':
        raise ValueError()
    element_frame:str = get_element_frame(tag.name,{},res)
    content = ''
    if tag.contents:
        for child in tag:
            if isinstance(child,str) or child.name != 'p':
                continue
            for grand_child in child:
                content += element2xaml_general(grand_child,res)
    return element_frame.replace('${content}',content)

def element2xaml_general(tag,res):
    '''元素转为xaml代码通用入口'''
    if isinstance(tag,str):
        return encode_escape(tag)
    match tag.name:
        case 'li':
            return list_item2xaml(tag,res)
        case 'blockquote':
            return quote2xaml(tag,res)
        case _:
            return common2xaml(tag,res)

def common2xaml(tag,res):
    '''一般元素转为xaml代码'''
    name = tag.name
    attrs = tag.attrs
    content = ''
    remove_wrapper = False #删除本节点，将子节点替换该节点的位置
    element_frame:str = get_element_frame(name,attrs,res)
    if element_frame is None:
        return str(tag)
    if tag.contents:
        if name == 'p':
            content += FIRSTLINE_SPACES
            if len(tag.contents) == 1 and tag.contents[0].name == 'img':
                remove_wrapper = True
        for child in tag.contents:
            content += element2xaml_general(child,res)
    if remove_wrapper:
        return content
    return element_frame.replace('${content}',content)

def html2xaml(html,res):
    '''html转为xaml代码'''
    soup = BeautifulSoup(html,'html.parser')
    xaml = ''
    for tag in soup.find_all(recursive=False):
        xaml += element2xaml_general(tag,res)
    return xaml

del_pattern = re.compile(r'~~(.*)~~')

def md_del_replace(md:str):
    '''转译删除线'''
    return re.sub(del_pattern,r'<del>\1</del>',md)

def convert(card,res):
    '''生成xaml代码'''
    md = card['markdown']
    md = md_del_replace(md)
    html = markdown.markdown(md)
    xaml = html2xaml(html,res)
    return xaml

@script('MarkdownPresenter')
def script(card,res,**_):
    '''从markdown生成xaml代码脚本'''
    return convert(card,res)
