from typing import Dict, Set, TypedDict, TYPE_CHECKING
from Builder.Core.utils import PropertySetter
from Builder.Core.resource import Resource

if TYPE_CHECKING:
    from . import Builder, Project
    from Core.elements import Component

class BuildingEnvironment(TypedDict):
    """构建时环境"""
    builder: 'Builder'
    """环境构建器"""
    project: 'Project'
    """所在工程"""
    resources: Dict[str,Resource]
    """工程资源"""
    components: Dict[str,'Component']
    data: Dict[str,object]
    page_templates: Dict[str,str]
    setter: PropertySetter
    used_resources: Set[str] = set()
