import markdown
import re
from bs4 import BeautifulSoup
from Core.Debug import LogInfo

def get_replacement(name:str,attrs:dict):
    component_name = name
    replace_list = []
    if name == 'h1':
        return (None,None)
    if name[0] == 'h' and name[1:].isdigit():
        component_name = 'h'
        replace_list.append(('level',name[1:]))
    elif name == 'a':
        replace_list.append(('link',attrs['href'])) 
    return (component_name, replace_list)

def get_element_frame(name,attrs,res):
    components:dict[str,str] = res.components
    component_name, replace_list = get_replacement(name,attrs)
    if component_name == None: # e.g H1
        return ''
    replace_str = components.get(component_name)
    if replace_str is None:
        LogInfo(f'[Marodown] markdown 中存在尚不支持的元素{name}')
        return None
    for k,v in replace_list:
        replace_str = replace_str.replace(f'${{{k}}}',replace_esc_char(v))
    return replace_str
    
FIRSTLINE_SPACES = '    '
LINE_BREAK = '<LineBreak/>'
INLINE_ELEMENTS = ['li','p','em','strong','a','code','del']

def is_inline(tag):
    if isinstance(tag,str):
        return True
    return tag.name in INLINE_ELEMENTS

def listItem2xaml(tag,res): 
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
                    content += replace_esc_char(child)
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
    if isinstance(tag,str):
        return replace_esc_char(tag)
    match tag.name:
        case 'li':
            return listItem2xaml(tag,res)
        case 'blockquote':
            return quote2xaml(tag,res)
        case _:
            return common2xaml(tag,res)

def common2xaml(tag,res):
    name = tag.name
    attrs = tag.attrs
    content = ''
    element_frame:str = get_element_frame(name,attrs,res)
    if element_frame is None:
        return str(tag)
    if tag.contents:
        if name == 'p':
                content += FIRSTLINE_SPACES
        for child in tag.contents:
            content += element2xaml_general(child,res)
    return element_frame.replace('${content}',content)

def html2xaml(html,res):
    soup = BeautifulSoup(html,'html.parser')
    xaml = ''
    for tag in soup.find_all(recursive=False):
        xaml += element2xaml_general(tag,res)
    return xaml

def replace_esc_char(string:str):
    for key in esc_chars:
        string = string.replace(key,esc_chars[key])
    return string

del_pattern = re.compile(r'~~(.*)~~')

def md_del_replace(md:str):
    return re.sub(del_pattern,r'<del>\1</del>',md)

def convert(card,res):
    md = card['data']
    md = md_del_replace(md)
    html = markdown.markdown(md)
    xaml = html2xaml(html,res)
    return xaml

def script(card,args,res):
    return convert(card,res)

esc_chars = {
    '<':'&lt;',
	'>':'&gt;',
	'"':'&quot;',
	"'":'&apos;',
	'¡':'&iexcl;',
	'¢':'&cent;',
	'£':'&pound;',
	'¤':'&curren;',
	'¥':'&yen;',
	'¦':'&brvbar;',
	'§':'&sect;',
	'¨':'&uml;',
	'©':'&copy;',
	'ª':'&ordf;',
	'«':'&laquo;',
	'¬':'&not;',
	'®':'&reg;',
	'¯':'&macr;',
	'°':'&deg;',
	'±':'&plusmn;',
	'²':'&sup2;',
	'³':'&sup3;',
	'´':'&acute;',
	'µ':'&micro;',
	'¶':'&para;',
	'·':'&middot;',
	'¸':'&cedil;',
	'¹':'&sup1;',
	'º':'&ordm;',
	'»':'&raquo;',
	'¼':'&frac14;',
	'½':'&frac12;',
	'¾':'&frac34;',
	'¿':'&iquest;',
    '&':'&amp;'
}