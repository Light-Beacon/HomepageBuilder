from typing import Union,List
from Interfaces import encode_escape,Logger

logger = Logger('Markdown')
FIRSTLINE_SPACES = '    '

class Node(): 
    def __init__(self,tag,res,parent_stack):
        self.res = res
        self.name = tag.name
        self.attrs = tag.attrs
        self.tag = tag
        self.children = None
        self.parent_stack = parent_stack
        self.expose = False
        self.self_break = False
    
    @property
    def inline(self) -> bool:
        raise NotImplementedError()
    
    @property
    def isblock(self) -> bool:
        return False
    
    @property
    def component_name(self) -> str:
        '''对应组件的名称'''
        return self.name
        
    def get_replacement(self) -> Union[List|None]:
        '''获取替换框架占位符的字符串列表'''
        return None

    def get_element_frame(self):
        '''获取元素框架'''
        components:dict[str,str] = self.res.components
        replace_list = self.get_replacement()
        replace_str = components.get(self.component_name)
        if replace_list:
            for k,v in replace_list:
                replace_str = replace_str.replace(f'${{{k}}}',encode_escape(v))
        return replace_str
    
    def parse_children(self):
        if self.tag.contents:
            self.children = []
            for child in self.tag.contents:
                self.add_child_node(create_node(child,self.parent_stack + self))
                
    def add_child_node(self,child_node:'node'):
        if child_node.expose:
            self.self_break = True
        self.children += child_node
    
    def prase_children(self):
        content = ''
        for child in self.children:
            content += child.prase()
        return content
    
    def prase(self):
        element_frame:str = self.get_element_frame(self.res)
        if element_frame is None:
            return str(self.tag)
        content = self.prase_children() if self.children else ''
        if self.self_break:
            return content
        return element_frame.replace('${content}',content)
    
class inlineNode(Node):
    @property
    def inline(self):
        return True
    
class lineNode(Node):
    @property
    def inline(self):
        return False
    
class blockNode(Node):
    @property
    def isblock(self):
        return True

class Text(inlineNode):
    def __init__(self,content,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.content = content
    
    def prase(self):
        return encode_escape(self.content)

    def __eq__(self,cmp):
        return cmp == self.content
    
class MarkdownListItem(lineNode):
    def prase_children(self):
        content = ''
        in_paragraph = False
        for child in self.children:
            if child.inline:
                if child == '\n':
                    continue
                if not in_paragraph:
                    content += '<Paragraph>'
                    in_paragraph = True
            else:
                if in_paragraph:
                    content += '</Paragraph>'
                    in_paragraph = False
            content += child.prase()
        if in_paragraph:
            content += '</Paragraph>'
        return content

class Qoute(lineNode):
    def prase_children(self):
        for child in self.children:
            if child.name != 'p':
                continue
            for grand_child in child.children:
                content += grand_child.prase()
                
class Paragraph(lineNode):
    def prase_children(self):                
        inblock = False
        content = FIRSTLINE_SPACES
        for child in self.children:
            if not child.isblock:
                if inblock:
                    inblock = False
                    content += '<Paragraph>'
                content += child.prase()
                continue
            else:
                if not inblock:
                    inblock = True
                    content += '</Paragraph>'
                    content += child.prase()
        if inblock:
            content += '<Paragraph>'

class Heading(lineNode):
    @property
    def component_name(self) -> str:
        return 'heading'
        
    def get_replacement(self) -> Union[List|None]:
        return[('level',self.name[1:])]

class Link(inlineNode):   
    def get_replacement(self) -> Union[List|None]:
        return[('link',self.attrs['href'])]

class MarkdownImage(blockNode):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title = self.attrs.get('title')
        
    @property
    def component_name(self) -> str:
        return 'titled-img' if self.title else 'img'
    
    def get_replacement(self) -> Union[List|None]:
        replace_list = []
        replace_list.append(('source',self.attrs['src']))
        if self.title:
            replace_list.append(('title',self.title))