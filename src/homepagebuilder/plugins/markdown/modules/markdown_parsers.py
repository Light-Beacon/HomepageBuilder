from typing import Union,List,Literal,Dict
from abc import abstractmethod,ABC
from enum import Enum
import re 
from homepagebuilder.interfaces import encode_escape,Logger

logger = Logger('Markdown')
FIRSTLINE_SPACES = '    '

TAG_PARSER_MAPPING = {}

def handles(*args):
    def wrapper(cls):
        for name in args:
            TAG_PARSER_MAPPING[name] = cls
        return cls
    return wrapper

def find_first_text(node:'Node',regex:Union[re.Pattern|None],
                    remove:bool = False) -> Union[str|None]:
    '''寻找节点中符合要求的最开始的文本'''
    for child in node.children:
        if isinstance(child,Text):
            if len(text := child.content.replace('\n','')) > 0:
                # 找到了文本
                if not regex:
                    if remove:
                        child.content = ''
                    return text
                else:
                    if matches := re.match(regex,text):
                        text = matches.group(1)
                        if remove:
                            child.content = child.content.replace(matches.group(0),'',1)
                        return text
        else:
            if text := find_first_text(child,regex,remove):
                return text
    return None

def to_plain_str(node:'Node') -> str:
    content = ''
    for child in node.children:
        if isinstance(child,Text):
            content += child.content
        else:
            content += to_plain_str(child)
    return content

class NodeType(Enum):
    ANY = -1
    UNDEFINED = 0
    PLAINTEXT = 1
    BLOCK = 2
    INLINE = 3
    UIELEMENT = 4

class Node():
    def __init__(self,tag,env,parent_stack):
        self.env = env
        self.components = env.get('components')
        self.name:str = None
        self.attrs = None
        self.tag = tag
        self.children:List['Node'] = None
        self.parent_stack:List['Node'] = parent_stack
        self.expose:bool = False
        self.self_break:bool = False
        self.parse_children()

    @property
    def ancestor(self) -> 'Node':
        if len(self.parent_stack) > 0:
            return self.parent_stack[-1]
        else:
            return None

    @property
    def component_name(self) -> str:
        '''对应组件的名称'''
        return self.name

    @abstractmethod
    def get_replacement(self) -> Union[Dict|None]:
        '''获取替换框架占位符的字符串字典'''

    @abstractmethod
    def get_element_frame(self) -> str:
        '''获取元素框架'''

    @abstractmethod
    def parse_children(self) -> None:
        '''解析子元素'''

    @abstractmethod
    def add_child_node(self,child_node:'Node') -> None:
        '''增加子节点'''

    @abstractmethod
    def convert_children(self) -> str:
        '''获取子节点的xaml代码'''

    @abstractmethod
    def convert(self) -> str:
        '''获取本节点的xaml代码'''

    @property
    def contain_type(self) -> NodeType:
        '''本节点的子元素类型'''
        return NodeType.UNDEFINED

    @property
    def node_type(self) -> NodeType:
        '''本节点的类型'''
        raise NodeType.UNDEFINED

class VoidNode(Node):
    def get_replacement(self):
        return None

    def get_element_frame(self):
        return ''

    def parse_children(self):
        pass

    def add_child_node(self,_):
        raise NotImplementedError()

    def convert_children(self):
        return ''

    def convert(self) -> str:
        return ''

class NodeBase(Node): 
    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag, *args, **kwargs)
        if tag:
            self.name = tag.name
            self.attrs = tag.attrs
            self.parse_children()

    def get_replacement(self) -> Dict:
        return {}

    def get_element_frame(self):
        replacement = self.get_replacement()
        component_obj = self.components.get(self.component_name)
        component_obj.mark_used_resources(replacement,self.env)
        replace_str = str(component_obj)
        if len(replacement) > 0:
            for k,v in replacement.items():
                replace_str = replace_str.replace(f'${{{k}}}',encode_escape(str(v)))
        return replace_str

    def parse_children(self):
        if self.tag.contents:
            self.children = []
            for child in self.tag.contents:
                self.add_child_node(create_node(child,self.env,self.parent_stack + [self]))

    def add_child_node(self,child_node:Node):
        if child_node.expose:
            self.self_break = True
        self.children.append(child_node)

    def convert_children(self):
        content = ''
        for child in self.children:
            content += child.convert()
        return content

    def convert(self):
        content = self.convert_children() if self.children else ''
        if self.self_break:
            return content
        element_frame:str = self.get_element_frame()
        return element_frame.replace('${content}',content)

class InlineNode(NodeBase):
    """行内元素"""
    @property
    def node_type(self):
        return NodeType.INLINE

class BlockNode(NodeBase):
    """块元素"""
    @property
    def node_type(self):
        return NodeType.BLOCK

class InlineNodeContainer(NodeBase):
    """行内元素容器"""
    @property
    def contain_type(self):
        return NodeType.INLINE

class BlockNodeContainer(NodeBase):
    """块元素容器"""
    @property
    def contain_type(self):
        return NodeType.BLOCK

class WPFUIElement(NodeBase):
    """WPF UI 元素"""
    @property
    def node_type(self):
        return NodeType.UIELEMENT

class WPFUIContainer(NodeBase):
    """WPF UI 自动容器"""
    @property
    def node_type(self):
        return NodeType.ANY

    def convert(self):
        if self.ancestor.contain_type == NodeType.INLINE:
            return "<InlineUIContainer>" + super().convert() + "</InlineUIContainer>"
        elif self.ancestor.contain_type == NodeType.BLOCK:
            return "<BlockUIContainer>" + super().convert() + "</BlockUIContainer>"
        else:
            raise TypeError

@handles('em','strong','code','del','br')
class CommonInlineNode(InlineNode, InlineNodeContainer):
    """通用行内元素"""

@handles('hr','ul','ol')
class CommonBlockNode(BlockNode, InlineNodeContainer):
    """通用块元素"""

class Text(VoidNode):
    def __init__(self,tag,*args,**kwargs):
        super().__init__(tag,*args,**kwargs)
        self.content = str(tag)

    def convert(self):
        return encode_escape(self.content)

    def isempty(self):
        return len(self.content) == 0

    def isblank(self):
        return len(self.content
                   .replace(" ",'')
                   .replace("\n",'')
                   .replace("\r",'')
                   .replace("\t",'')) == 0
    
    @property
    def node_type(self):
        return NodeType.PLAINTEXT

    def __eq__(self,cmp):
        return cmp == self.content

    def __format__(self, format_spec):
        return f'<MarkdownText content="{self.content}">'

    def __str__(self):
        return f'<MarkdownText content="{self.content}">'
@handles('p')
class Paragraph(BlockNode, InlineNodeContainer):
    pass

class ListItemParagraph(Paragraph):
    def __init__(self,children,env, parent_stack ):
        super().__init__(tag = None, env = env, parent_stack=parent_stack)
        self.children = children

    def parse_children(self,*args,**kwargs):
        pass

    @property
    def component_name(self):
        return 'listitempara'

@handles('li')
class MarkdownListItem(BlockNode, BlockNodeContainer):
    children_paragraph_class = ListItemParagraph
    def parse_children(self):
        super().parse_children()
        inline_children_buffer = []
        new_children = []
        for child in self.children:
            if child.node_type == NodeType.PLAINTEXT:
                if isinstance(child,Text) and child.isblank():
                    continue
                inline_children_buffer.append(child)
            elif child.node_type == NodeType.INLINE:
                inline_children_buffer.append(child)
            else:
                if len(inline_children_buffer) > 0:
                    new_children.append(self.children_paragraph_class(
                        inline_children_buffer,env = self.env,
                        parent_stack = self.parent_stack + [self]))
                new_children.append(child)
        if len(inline_children_buffer) > 0:
            new_children.append(self.children_paragraph_class(
                inline_children_buffer,env = self.env,
                parent_stack = self.parent_stack + [self]))
        self.children = new_children


QUOTE_TYPE_PATTERN = re.compile(r'^\[!(.*)\]')
QUOTE_TYPE_NAMES = {
    'note': '注释',
    'tip': '提示',
    'important': '重要',
    'warning': '警告',
    'caution': '注意'
}
QUOTE_TYPE_ISWARN_MAPPING = {
    'info': False,
    'warn': True,
}

@handles('blockquote')
class Quote(BlockNode, BlockNodeContainer):
    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag, *args, **kwargs)
        quote_type = find_first_text(self,regex = QUOTE_TYPE_PATTERN,remove=True)
        self.quote_type = quote_type.lower() if quote_type else None
        self.quote_type_name = QUOTE_TYPE_NAMES.get(self.quote_type,quote_type)
        self.is_pcl_hint = self.quote_type in QUOTE_TYPE_ISWARN_MAPPING
        self.is_warn = QUOTE_TYPE_ISWARN_MAPPING.get(self.quote_type,None)

    @property
    def component_name(self) -> str:
        if self.is_pcl_hint:
            return 'pclhint'
        if self.quote_type:
            return 'blockquote-typed'
        return 'blockquote'

    def get_replacement(self) -> Union[List]:
        if self.is_pcl_hint:
            return {'iswarn': self.is_warn}
        else:
            return {'type': self.quote_type,
                    'typename': self.quote_type_name}

    def convert_children(self):
        content = ''
        if self.is_pcl_hint:
            content = to_plain_str(self)
        else:
            content = super().convert_children()
        return content

@handles('h1','h2','h3','h4','h5')
class Heading(BlockNode):
    @property
    def component_name(self) -> str:
        return 'heading'

    def get_replacement(self) -> Union[List|None]:
        return {'level': self.name[1:]}

@handles('a')
class Link(InlineNode, InlineNodeContainer):
    def get_replacement(self) -> Union[List|None]:
        reps = {'link': self.attrs['href']}
        ancestor = self.ancestor
        if ancestor.name == 'li':
            reps['pos_down'] = 3
        else:
            reps['pos_down'] = 2
        return reps

@handles('img')
class MarkdownImage(WPFUIContainer):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title = self.attrs.get('title')

    @property
    def component_name(self) -> str:
        return 'titled-img' if self.title else 'img'

    def get_replacement(self) -> Union[List|None]:
        replacements = {'source': self.attrs['src']}
        if self.title:
            replacements['title'] = self.title
        return replacements

def create_node(tag,env,parent_stack):
    if isinstance(tag,str):
        return Text(tag,env=env,parent_stack=parent_stack)
    else:
        return TAG_PARSER_MAPPING[tag.name](tag=tag,env=env,parent_stack=parent_stack)