from typing import Union, Dict
import re
from homepagebuilder.interfaces import encode_escape
from .text import Text
from .base import Node, NodeType

FIRSTLINE_SPACES = '    '

TAG_PARSER_MAPPING = {}

def find_first_text(node:Node, regex:Union[re.Pattern|None],
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

def handles(*args):
    def wrapper(cls):
        for name in args:
            TAG_PARSER_MAPPING[name] = cls
        return cls
    return wrapper

def create_node_from_tag(tag,context,parent_stack):
    if isinstance(tag,str):
        return Text(tag,context=context,parent_stack=parent_stack)
    else:
        return TAG_PARSER_MAPPING[tag.name](tag=tag,context=context,parent_stack=parent_stack)

class NodeBase(Node): 
    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag, *args, **kwargs)
        self.escaping_special_chars: bool = False
        """是否转义 \\n \\r \\t"""
        if tag:
            self.name = tag.name
            self.attrs = tag.attrs
            self.parse_children()

    def get_replacement(self) -> Dict:
        return {}

    def get_element_frame(self):
        replacement = self.get_replacement()
        component_obj = self.components.get(self.component_name)
        if component_obj is None:
            raise ValueError(f'Componet not found: {self.component_name}')
        component_obj.mark_used_resources(replacement,self.context)
        replace_str = str(component_obj)
        if len(replacement) > 0:
            for k,v in replacement.items():
                replace_str = replace_str.replace(f'${{{k}}}',
                    encode_escape(str(v),with_special=self.escaping_special_chars))
        return replace_str

    def parse_children(self):
        if self.tag.contents:
            self.children = []
            for child in self.tag.contents:
                self.add_child_node(
                    create_node_from_tag(child,self.context,self.parent_stack + [self]))

    def add_child_node(self,child_node:Node):
        self.children.append(child_node)

    def convert_children(self):
        content = ''
        for child in self.children:
            content += child.convert()
        return content

    def convert(self):
        content = self.convert_children() if self.children else ''
        if self.expose_children:
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
        if not self.actual_ancestor or \
            self.actual_ancestor.contain_type in [NodeType.BLOCK, NodeType.ANY]:
            return "<BlockUIContainer>" + super().convert() + "</BlockUIContainer>"
        elif self.actual_ancestor.contain_type == NodeType.INLINE:
            return "<InlineUIContainer>" + super().convert() + "</InlineUIContainer>"
        else:
            raise TypeError
