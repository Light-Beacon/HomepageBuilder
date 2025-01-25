from typing import Dict, Set, TYPE_CHECKING
import copy

if TYPE_CHECKING:
    from . import Builder, Project
    from ..pages import PageBase
    from ...core.elements import Component
    from ..utils.property import PropertySetter
    from ..resource import Resource

class Context():
    """构建时环境"""

    def copy(self):
        """获取上下文的拷贝"""
        return copy.copy(self)

    builder: 'Builder'
    """构建器"""
    project: 'Project'
    """工程"""
    resources: Dict[str,'Resource']
    """工程资源"""
    components: Dict[str,'Component']
    """构件"""
    templates: Dict[str, Dict]
    """卡片模版"""
    data: Dict[str,object]
    """数据"""
    page_templates: Dict[str,str]
    """页面模版"""
    setter: 'PropertySetter'
    """设置器"""
    used_resources: Set[str] = set()
    """使用过的资源"""
    env: Dict = {}
    """环境字典"""
    page: PageBase
