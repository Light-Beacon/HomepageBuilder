import os
from .config import enable_by_config
from .IO import Dire
from .project import Project
from .i18n import locale as t, append_locale
from .logger import Logger
from .ModuleManager import load_module_dire,get_check_list
from .templates_manager import TemplateManager
from .types import Builder as BuilderBase
from .loader import Loader
from .utils import getbuilderpath
from ..Debug import global_anlyzer as anl

PATH_SEP = os.path.sep
logger = Logger('Builder')

class Builder(BuilderBase):
    """构建器核心"""
    def __init__(self):
        super().__init__()
        self.envpath = os.path.dirname(os.path.dirname(__file__))
        anl.phase('初始化构建器')
        anl.switch_in()
        anl.phase('加载基础资源')
        self.__init_env()
        self.load_structure(getbuilderpath('Resources/Structures/'))
        self.load_resources(getbuilderpath('Resources/Resources/'))
        self.template_manager = TemplateManager()
        self.load_modules(getbuilderpath('Modules'))
        self.load_plugins(getbuilderpath('Plugins'))
        self.current_project = None
        anl.switch_out()

    def __init_env(self):
        self.__env['components'] = {}
        self.__env['builder'] = self
        self.__env['data'] = {}
        self.__env['page_templates'] = {}
        self.__env['templates'] = {}
        self.__env['project'] = None
        self.__env['resources'] = {}
        self.__env['setter'] = None

    def load_structure(self,dire_path):
        anl.phase('加载结构文件')
        self.__env['components'].update(
            Loader.load_compoents(dire_path + 'Components'))
        self.__env['templates'].update(
            Loader.load_tempaltes(dire_path + 'Templates'))
        self.__env['page_templates'].update(
            Loader.load_page_tempaltes(dire_path + 'PageTemplates'))

    def load_resources(self,dire_path):
        """加载构建器资源"""
        anl.phase('加载资源文件')
        logger.info(t('builder.load.resources'))
        self.__env['resources'].update(
            Loader.load_resources(dire_path))

    def load_modules(self,dire_path):
        """加载构建器模块"""
        anl.phase('加载模块')
        logger.info(t('project.load.modules'))
        load_module_dire(dire_path)

    @enable_by_config('System.EnablePlugins')
    def load_plugins(self, plugin_path):
        """加载构建器插件"""
        anl.phase('加载插件')
        logger.info(t('project.load.plugins'))
        anl.switch_in()
        for file in Dire(plugin_path).scan_subdir(r'pack\.yml'):
            data = file.data
            anl.phase(file.data['pack_namespace'])
            anl.switch_in()
            dire = os.path.dirname(data['file_path'])
            anl.phase('加载插件结构')
            self.load_structure(f'{dire}{PATH_SEP}Structures/')
            anl.phase('加载插件资源')
            self.load_resources(f'{dire}{PATH_SEP}Resources')
            anl.phase('加载插件模块')
            load_module_dire(f'{dire}{PATH_SEP}Modules')
            anl.phase('加载插件本地化文件')
            append_locale(f'{dire}{PATH_SEP}i18n')
            anl.switch_out()
        self.__check_module_wait_list()
        anl.switch_out()

    def __check_module_wait_list(self):
        if len(wait_list := get_check_list()) > 0:
            logger.error(t('builder.check_module_list.error', wait_list=wait_list))

    def load_proejct(self,project_path):
        self.current_project = Project(self,project_path)