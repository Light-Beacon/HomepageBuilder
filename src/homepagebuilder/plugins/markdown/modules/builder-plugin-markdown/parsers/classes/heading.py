from typing import Union, List
from ..base import BlockNode
from ..utils import handles

@handles('h1','h2','h3','h4','h5')
class Heading(BlockNode):
    @property
    def component_name(self) -> str:
        return 'heading'

    def get_replacement(self) -> Union[List|None]:
        return {'level': self.name[1:]}