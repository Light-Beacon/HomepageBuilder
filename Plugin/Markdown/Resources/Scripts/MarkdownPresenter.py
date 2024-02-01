import markdown
from bs4 import BeautifulSoup
from . import Templates_Manager

def get_replacement(name:str):
    component_name = name
    replace_list = []
    if name[0] == 'h' and name[1:].isdigit():
        replace_list.append(('level',name[1:]))
        component_name = 'h'
    return (component_name, replace_list)

def replace(name,content,res):
    #print(name)
    components:dict[str,str] = res.components
    component_name, replace_list = get_replacement(name)
    replace_str = components.get(component_name)
    replace_str = replace_str.replace('${content}',content)
    #print(f'{replace_str} : {content}')
    for k,v in replace_list:
        #print(k+v+' ')
        replace_str = replace_str.replace(f'${{{k}}}',v)
    return replace_str
    
def tag2xaml(tag,res):
    name = tag.name
    content = ''
    if tag.contents:
        for child in tag.contents:
            if isinstance(child,str):
                content += child
            else:
                content += tag2xaml(child,res)
    return replace(name,content,res)

def html2xaml(html,res):
    soup = BeautifulSoup(html,'html.parser')
    xaml = ''
    for tag in soup.find_all(recursive=False):
        xaml += tag2xaml(tag,res)
    return xaml

def convert(md,res):
    html = markdown.markdown(md)
    return html2xaml(html,res)
    
def script(card,args,res):
    return convert(card['data'],res)