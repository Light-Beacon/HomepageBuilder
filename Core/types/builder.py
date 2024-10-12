from abc import ABC,abstractmethod
from Core.resource import Resource
from Core.templates_manager import TemplateManager

class Builder(ABC):
    """构建器核心"""
    def __init__(self) -> None:
        self.envpath: str
        self.resources: Resource
        self.template_manager: TemplateManager
        self.current_project: 'Project'


    @abstractmethod
    def load_resources(self,resources_dire_path) -> None:
        """加载构建器资源"""

    @abstractmethod
    def load_modules(self,modules_dire_path) -> None:
        """加载构建器模块"""

    @abstractmethod
    def load_plugins(self, plugin_path) -> None:
        """加载构建器插件"""

    @abstractmethod
    def load_proejct(self,project_path) -> None:
        """加载工程"""