from ..base import InlineNode, InlineNodeContainer, BlockNode
from ..utils import handles

@handles('em','strong','code','del','br')
class CommonInlineNode(InlineNode, InlineNodeContainer):
    """通用行内元素"""

@handles('hr','ul','ol')
class CommonBlockNode(BlockNode, InlineNodeContainer):
    """通用块元素"""
