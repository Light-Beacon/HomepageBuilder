import re
from typing import List, TYPE_CHECKING
from Core.utils import format_code

if TYPE_CHECKING:
    from Core.IO import File
    from Core.types import BuildingEnvironment

RESOURCE_PATTERN = re.compile(r'Style\s*=\s*\"\s*{\s*StaticResource\s+([^\s]*)\s*}\s*\"')

class Component:
    def __init__(self, file: 'File') -> None:
        self.file:File = file
        self.used_resources:List[str] = self.__findusedresources()

    def toxaml(self, card, env, children_code = '') -> str:
        self.mark_used_resources(card,env)
        return format_code(code = self.file.data,data = card,env=env,children_code=children_code)

    def __findusedresources(self):
        return RESOURCE_PATTERN.findall(self.file.data)

    def mark_used_resources(self,card,env:'BuildingEnvironment'):
        for res_ref in self.used_resources:
            res_ref = format_code(code = res_ref,data=card,env=env)
            env.get('used_styles').add(res_ref)

    def __str__(self) -> str:
        return self.file.data