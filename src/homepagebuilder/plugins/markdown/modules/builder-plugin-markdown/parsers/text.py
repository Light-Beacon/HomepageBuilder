from homepagebuilder.interfaces import encode_escape
from typing import Union
from .base import VoidNode, NodeType

class Text(VoidNode):
    def __init__(self,tag,*args,**kwargs):
        super().__init__(tag,*args,**kwargs)
        if tag:
            self.content = str(tag)

    @classmethod
    def from_str(cls, content:str):
        obj = cls(None)
        obj.content = content
        return obj

    def convert(self):
        return encode_escape(self.content)

    def isempty(self):
        """判断文本内容是否为空

        Returns:
            布尔值: 若文本内容为空则为真，否则为假
        """
        return len(self.content) == 0

    def isblank(self):
        """判断文本内容是否为空或仅由空白字符组成

        Returns:
            布尔值: 若文本内容为空或仅由空白字符组成则为真，否则为假
        """
        return len(self.content.strip()) == 0

    @property
    def node_type(self):
        return NodeType.PLAINTEXT

    def __eq__(self,cmp):
        return cmp == self.content

    def __format__(self, format_spec):
        return f'<MarkdownText content="{self.content}">'

    def __add__(self, text:Union[str, 'Text']):
        string = self.content
        if isinstance(text, Text):
            string += text.content
        elif isinstance(text, str):
            string += text
        else:
            raise TypeError
        return Text.from_str(string)

    def __str__(self):
        return f'<MarkdownText content="{self.content}">'

    def __len__(self):
        return len(self.content)