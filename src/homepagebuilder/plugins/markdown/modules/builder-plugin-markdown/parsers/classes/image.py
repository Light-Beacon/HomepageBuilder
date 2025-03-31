from typing import Union, List
from ..base import WPFUIContainer
from ..utils import handles

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
