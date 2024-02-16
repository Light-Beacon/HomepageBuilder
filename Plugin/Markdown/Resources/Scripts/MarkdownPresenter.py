import markdown
from bs4 import BeautifulSoup
from . import Templates_Manager
from .Debug import LogWarning

def get_replacement(name:str,attrs:dict):
    component_name = name
    replace_list = []
    if name[0] == 'h' and name[1:].isdigit():
        component_name = 'h'
        replace_list.append(('level',name[1:]))
    elif name == 'a':
        replace_list.append(('link',attrs['href']))
    return (component_name, replace_list)

def replace(name,attrs,content,res):
    #print(name)
    components:dict[str,str] = res.components
    component_name, replace_list = get_replacement(name,attrs)
    replace_str = components.get(component_name)
    if replace_str is None:
        LogWarning(f'[Marodown] markdown 中存在尚不支持的元素{name}')
        return None
    replace_str = replace_str.replace('${content}',content)
    #print(f'{replace_str} : {content}')
    for k,v in replace_list:
        #print(k+v+' ')
        replace_str = replace_str.replace(f'${{{k}}}',v)
    return replace_str
    
def tag2xaml(tag,res):
    name = tag.name
    attrs = tag.attrs
    content = ''
    if tag.contents:
        for child in tag.contents:
            if isinstance(child,str):
                # FIX NEWLINE ERROR
                if child == '\n':
                    continue
                content += replace_esc_char(child)
                if tag.name == 'li':
                    content += '<LineBreak/>'
            else:
                content += tag2xaml(child,res)
                if tag.name == 'li' and child.name == 'ul':
                    content += '<LineBreak/>'
    if tag.name == 'ul':
        content = content.split('<LineBreak/>')
        while len(content[-1]) == 0:
            content = content[:-1]
        content = '<LineBreak/>'.join(content)
    replacement:str = replace(name,attrs,content,res)
    if replacement is None:
        return str(tag)
    return replacement

def html2xaml(html,res):
    soup = BeautifulSoup(html,'html.parser')
    xaml = ''
    for tag in soup.find_all(recursive=False):
        xaml += tag2xaml(tag,res)
    return xaml

def replace_esc_char(string:str):
    for key in esc_chars:
        string = string.replace(key,esc_chars[key])
    return string
    
def convert(md,res):
    md = replace_esc_char(md)
    html = markdown.markdown(md)
    xaml = html2xaml(html,res)
    return xaml

def script(card,args,res):
    return convert(card['data'],res)

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
}