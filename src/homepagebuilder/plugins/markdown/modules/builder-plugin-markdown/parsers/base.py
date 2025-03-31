from enum import Enum
from typing import List, Dict, Union
from abc import abstractmethod

class NodeType(Enum):
    ANY = -1
    UNDEFINED = 0
    PLAINTEXT = 1
    BLOCK = 2
    INLINE = 3
    UIELEMENT = 4

class Node():
    def __init__(self,tag,context,parent_stack):
        self.context = context
        self.components = context.components
        self.name:str = None
        self.attrs = None
        self.tag = tag
        self.children:List['Node'] = None
        self.parent_stack:List['Node'] = parent_stack
        self.expose_children:bool = False
        """隐藏本元素，将子元素设为与本元素同级"""

    @classmethod
    def create_from_html_tag(cls, tag, context, parent_stack):
        obj = cls(tag, context, parent_stack)
        obj.tag = tag
        return obj

    @property
    def ancestor(self) -> 'Node':
        """逻辑祖先"""
        if len(self.parent_stack) > 0:
            return self.parent_stack[-1]
        else:
            return None

    @property
    def actual_ancestor(self) -> 'Node':
        """**实际在xaml中体现的祖先**
        
        若逻辑祖先的 `expose_children` 为 true，则返回逻辑祖先的实际祖先
        """
        if ancestor := self.ancestor:
            if ancestor.expose_children:
                return ancestor.actual_ancestor
            else:
                return ancestor
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


