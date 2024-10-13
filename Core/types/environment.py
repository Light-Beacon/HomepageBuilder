from typing import Dict, Set, TypedDict, Union, TYPE_CHECKING
from Core.resource import Resource
from Core.utils import PropertySetter

if TYPE_CHECKING:
    from . import Builder, Project
    from Core.elements import Component

class BuildingEnvironment(TypedDict):
    """构建时环境"""
    builder: 'Builder'
    """环境构建器"""
    project: 'Project'
    """所在工程"""
    resource: Resource
    """工程资源"""
    animations: Dict[str,str]
    components: Dict[str,'Component']
    data: Dict[str,object]
    page_templates: Dict[str,str]
    templates: Dict[str,Dict]
    styles: Dict[str,Union[str,Dict]]
    setter: PropertySetter
    used_styles: Set[str] = set()
