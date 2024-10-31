import re
from typing import List
from ..io import File

RESOURCE_PATTERN = re.compile(r'\"\s*{\s*StaticResource\s+([^\s]*)\s*}\s*\"')
#RESOURCE_PATTERN = re.compile(r'Style\s*=\s*\"\s*{\s*StaticResource\s+([^\s]*)\s*}\s*\"')

def find_using_resources(target) -> List[str]:
    if isinstance(target,File):
        return RESOURCE_PATTERN.findall(target.data)
    elif isinstance(target,str):
        return RESOURCE_PATTERN.findall(target)
    else:
        raise TypeError()
