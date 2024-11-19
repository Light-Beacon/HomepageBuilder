from typing import List, TYPE_CHECKING
from ..utils.finder import find_using_resources
from ..formatter import format_code

if TYPE_CHECKING:
    from core.io import File
    from core.types import Context

class Component:
    def __init__(self, file: 'File') -> None:
        self.file:File = file
        self.used_resources:List[str] = self.__findusedresources()

    def toxaml(self, card, context, children_code = '') -> str:
        self.mark_used_resources(card,context)
        return format_code(code = self.file.data,data = card,context=context,children_code=children_code)

    def __findusedresources(self):
        return find_using_resources(self.file)

    def mark_used_resources(self,card,context:'Context'):
        for res_ref in self.used_resources:
            res_ref = format_code(code = res_ref,data=card,context=context)
            context.used_resources.add(res_ref)

    def __str__(self) -> str:
        return self.file.data