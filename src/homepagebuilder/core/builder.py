import os
from pathlib import Path
from typing import TYPE_CHECKING, Optional
from .config import enable_by_config
from .io import Dire
from .project import Project
from .i18n import locale as t, append_locale
from .logger import Logger
from .module_manager import load_module_dire,get_check_list
from .templates_manager import TemplateManager
from .loader import Loader
from .utils.paths import getbuilderpath
from ..core.types import Context
from .utils.property import PropertySetter

if TYPE_CHECKING:
    from ..core.resource import Resource
    from ..core.templates_manager import TemplateManager

PATH_SEP = os.path.sep
logger = Logger('Builder')

class Builder():
    """构建器核心"""

    def __init__(self):
        logger.info(t('builder.init'))
        self.envpath: str
        self.resources: Resource
        self.template_manager: TemplateManager
        self.__context:Context = Context()
        self.__context.builder = self
        self.envpath = os.path.dirname(os.path.dirname(__file__))
        self.__init_context()
        logger.info(t('builder.load.structures'))
        self.load_structure(getbuilderpath('resources/structures/'))
        logger.info(t('builder.load.resources'))
        self.load_resources(getbuilderpath('resources/resources/'))
        self.template_manager = TemplateManager()
        logger.info(t('builder.load.modules'))
        self.load_modules(getbuilderpath('modules'))
        self.load_plugins(getbuilderpath('plugins'))
        self.current_project: Optional[Project] = None

    def __init_context(self):
        self.__context.components = {}
        self.__context.builder = self
        self.__context.data = {}
        self.__context.page_templates = {}
        self.__context.templates = {}
        self.__context.project = None
        self.__context.resources = {}
        self.__context.setter = PropertySetter()

    def load_structure(self, dire_path:Path):
        """加载构建器结构"""
        self.__context.components.update(
            Loader.load_compoents(dire_path / 'components'))
        self.__context.templates.update(
            Loader.load_templates(dire_path / 'templates'))
        self.__context.page_templates.update(
            Loader.load_page_templates(dire_path / 'pagetemplates'))

    def load_resources(self,dire_path):
        """加载构建器资源"""
        self.__context.resources.update(
            Loader.load_resources(dire_path))

    def load_data(self, dire_path):
        """加载构建器数据"""
        self.__context.data.update(Loader.create_structure_mapping(dire_path))

    def load_modules(self,dire_path):
        """加载构建器模块"""
        load_module_dire(dire_path, context = self.__context)

    @enable_by_config('System.EnablePlugins')
    def load_plugins(self, plugin_path):
        """加载构建器插件"""
        logger.info(t('builder.load.plugins'))
        for file in Dire(plugin_path).scan_subdir(r'pack\.yml'):
            plugin_logger = Logger(f'Plugin|{file.dire.name}')
            plugin_logger.info(t('plugin.init'))
            data = file.data
            dire = Path(data['file_path']).parent
            plugin_logger.debug(t('plugin.load.data'))
            self.load_data(dire / 'data')
            plugin_logger.debug(t('plugin.load.structures'))
            self.load_structure(dire / 'structures')
            plugin_logger.debug(t('plugin.load.resources'))
            self.load_resources(dire / 'resources')
            plugin_logger.debug(t('plugin.load.modules'))
            load_module_dire(dire / 'modules', context=self.__context)
            append_locale(dire / 'i18n')
        self.__check_module_wait_list()

    def __check_module_wait_list(self):
        if len(wait_list := get_check_list()) > 0:
            logger.error(t('builder.check_module_list.error', wait_list=wait_list))

    def load_project(self, project_path: 'Path'):
        """加载工程"""
        self.current_project = Project(self, project_path)

    def get_context_copy(self) -> 'Context':
        """获取环境拷贝"""
        return self.__context.copy()
    
    def get_data(self, key):
        return self.__context.data.get(key)

    def set_data(self, key, value):
        self.__context.data[key] = value