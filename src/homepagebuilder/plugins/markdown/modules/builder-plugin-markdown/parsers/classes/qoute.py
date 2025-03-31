import re
from typing import Union, List
from ..base import BlockNode, BlockNodeContainer
from ..utils import handles, find_first_text, to_plain_str

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

@handles('blockcode')
class BlockCode(BlockNode):
    """块状代码块"""
    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag, *args, **kwargs)
        self.escaping_special_chars = True
    
    @property
    def component_name(self) -> str:
        return 'blockcode'
    
    def get_replacement(self) -> Union[List|None]:
        replacements = {'language': self.attrs['lang'],
                        'code': self.attrs['code']}
        return replacements
    

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
