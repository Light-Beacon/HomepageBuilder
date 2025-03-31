from ..base import InlineNodeContainer, BlockNode, NodeType
from ..utils import handles

@handles('p')
class Paragraph(BlockNode, InlineNodeContainer):
    @classmethod
    def from_inline_list(cls,inline_list,context,parent_stack):
        p = Paragraph(tag = None,context=context,parent_stack=parent_stack)
        p.children = inline_list
        p.name = 'p'
        return p

    def parse_children(self,*args,**kwargs):
        # 尽量让子元素以块状呈现
        super().parse_children(*args,**kwargs)
        children_buffer_inline = []
        new_children = []
        replace_children_flag = False
        for child in self.children:
            if child.node_type in [NodeType.BLOCK, NodeType.ANY]:
                self.expose_children = True
                replace_children_flag = True
                new_children.append(Paragraph.from_inline_list(
                    children_buffer_inline, context=self.context,
                    parent_stack=self.parent_stack))
                new_children.append(child)
                children_buffer_inline = []
            else:
                children_buffer_inline.append(child)   
        if replace_children_flag:
            new_children.append(Paragraph.from_inline_list(
                children_buffer_inline, context=self.context,
                parent_stack=self.parent_stack))
            self.children = new_children

class ListItemParagraph(Paragraph):
    def __init__(self,children,context, parent_stack ):
        super().__init__(tag = None, context = context, parent_stack=parent_stack)
        self.children = children

    def parse_children(self,*args,**kwargs):
        pass

    @property
    def component_name(self):
        return 'listitempara'