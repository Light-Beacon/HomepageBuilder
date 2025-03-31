from ..base import BlockNode, BlockNodeContainer, NodeType
from ..utils import handles
from .paragraph import ListItemParagraph
from ..text import Text

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
                        inline_children_buffer,context = self.context,
                        parent_stack = self.parent_stack + [self]))
                    inline_children_buffer = []
                new_children.append(child)
        if len(inline_children_buffer) > 0:
            new_children.append(self.children_paragraph_class(
                inline_children_buffer,context = self.context,
                parent_stack = self.parent_stack + [self]))
        self.children = new_children