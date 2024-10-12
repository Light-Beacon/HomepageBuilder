import os
from Core.config import enable_by_config
from Core.IO import Dire
from Core.project import Project
from Core.resource import Resource
from Debug import global_anlyzer as anl
from .i18n import locale as t
from .logger import Logger
from .ModuleManager import load_module_dire,get_check_list
from .templates_manager import TemplateManager
from .types import Builder as BuilderBase

PATH_SEP = os.path.sep
logger = Logger('Builder')

class Builder(BuilderBase):
    """构建器核心"""
    def __init__(self):
        self.envpath = os.path.dirname(os.path.dirname(__file__))
        anl.phase('初始化构建器')
        anl.switch_in()
        anl.phase('加载基础资源')
        self.resources = Resource()
        self.load_resources(f'{self.envpath}{PATH_SEP}Resources')
        self.template_manager = TemplateManager(self)    
        self.load_modules(f'{self.envpath}{PATH_SEP}Modules')
        self.load_plugins(f'{self.envpath}{PATH_SEP}Plugin')
        self.current_project = None
        anl.switch_out()

    def load_resources(self,resources_dire_path):
        """加载构建器资源"""
        anl.phase('加载资源')
        logger.info(t('builder.load.resources'))
        self.resources.load_resources(resources_dire_path)

    def load_modules(self,modules_dire_path):
        """加载构建器模块"""
        anl.phase('加载模块')
        logger.info(t('project.load.modules'))
        load_module_dire(modules_dire_path)

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
            anl.phase('加载插件资源')
            dire = os.path.dirname(data['file_path'])
            self.resources.load_resources(f'{dire}{PATH_SEP}Resources')
            anl.phase('加载插件模块')
            load_module_dire(f'{dire}{PATH_SEP}Modules', self)
            anl.switch_out()
        self.__check_module_wait_list()
        anl.switch_out()

    def __check_module_wait_list(self):
        if len(wait_list := get_check_list()) > 0:
            logger.error(t('builder.check_module_list.error', wait_list=wait_list))

    def load_proejct(self,project_path):
        self.current_project = Project(self,project_path)