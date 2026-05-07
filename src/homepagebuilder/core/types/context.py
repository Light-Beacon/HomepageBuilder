from typing import Dict, Set, TYPE_CHECKING, Union
import copy

if TYPE_CHECKING:
    from ..builder import Builder
    from ..project import Project
    from ...core.elements import Component
    from ..utils.property import PropertySetter
    from ..utils.client import PCLClient
    from ..resource import Resource
    from ...server.project_api import ProjectAPI
    from flask import Flask



class Context():
    """构建时环境"""

    def copy(self):
        """获取上下文的拷贝"""
        return copy.copy(self)

    builder: 'Builder'
    """构建器"""
    project: Union['Project', None]
    """工程"""
    resources: Dict[str,'Resource']
    """工程资源"""
    components: Dict[str,'Component']
    """构件"""
    templates: Dict[str, Dict]
    """卡片模版"""
    data: Dict[str,object] = {}
    """数据"""
    page_templates: Dict[str,str]
    """页面模版"""
    styles: Dict[str,object] = {}
    """样式"""
    setter: 'PropertySetter'
    """设置器"""
    server_api: 'ProjectAPI'
    """服务器 API"""
    flask_app: 'Flask'
    """Flask App"""
    client: 'PCLClient'
    """客户端信息"""
    used_resources: Set[str] = set()
    """使用过的资源"""

    @classmethod
    def get_current_context(cls) -> 'Context':
        """获取当前上下文"""
        return _CURRENT_CONTEXT

    @classmethod
    def set_current_context(cls, context: 'Context'):
        """设置当前上下文"""
        global _CURRENT_CONTEXT
        _CURRENT_CONTEXT = context

_CURRENT_CONTEXT = Context()