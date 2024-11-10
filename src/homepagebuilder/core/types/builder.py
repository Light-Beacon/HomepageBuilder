from abc import ABC,abstractmethod
from typing import TYPE_CHECKING
from .environment import BuildingEnvironment

if TYPE_CHECKING:
    from . import Project
    from ...core.resource import Resource
    from ...core.templates_manager import TemplateManager

class Builder(ABC):
    """构建器核心"""
    def __init__(self) -> None:
        self.envpath: str
        self.resources: Resource
        self.template_manager: TemplateManager
        self.current_project: Project
        self.__env:BuildingEnvironment = BuildingEnvironment(
            builder=self
        )

    @abstractmethod
    def load_resources(self,dire_path) -> None:
        """加载构建器资源"""

    @abstractmethod
    def load_modules(self,dire_path) -> None:
        """加载构建器模块"""

    @abstractmethod
    def load_plugins(self, plugin_path) -> None:
        """加载构建器插件"""

    @abstractmethod
    def load_proejct(self,project_path) -> None:
        """加载工程"""

    def get_environment_copy(self) -> 'BuildingEnvironment':
        """获取环境拷贝"""
        return self.__env.copy()