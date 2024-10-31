"""
工程文件模块，构建器核心
"""
import os
from .io import Dire, File
from .library import Library
from .logger import Logger
from .i18n import locale as t
from .module_manager import load_module_dire,get_check_list
from .utils.event import set_triggers
from .utils.paths import fmtpath
from ..debug import global_anlyzer as anl
from .page import CardStackPage, RawXamlPage
from .loader import Loader
from .types import Project as ProjectBase
from .config import import_config_dire
PATH_SEP = os.path.sep
logger = Logger('Project')

class Project(ProjectBase):
    """工程类"""
    def __checkModuleWaitList(self):
        if len(wait_list := get_check_list()) > 0:
            logger.error(t('project.check_module_list.error', wait_list=wait_list))

    @set_triggers('project.import')
    def import_pack(self, path):
        """导入工程包"""
        anl.phase('加载工程包')
        anl.switch_in()
        logger.info(t('project.import.start', path=path))
        self.__init_load_projectfile(path)
        self.__init_import_configs()
        self.__init_import_modules()
        self.__init_import_structures()
        self.__init_import_resources()
        self.__init_import_cards()
        self.__init_import_pages()
        self.__init_import_data()
        anl.switch_out()
        logger.info(t('project.import.success'))

    @set_triggers('project.import.projectfile')
    def __init_load_projectfile(self,path):
        anl.phase('读取工程文件')
        pack_info = File(path).read()
        self.base_path = os.path.dirname(path)
        self.version = pack_info['version']
        self.default_page = pack_info.get('default_page')
        logger.info(t('project.import.pack.version', version=self.version))

    def  __init_import_configs(self):
        anl.phase('导入配置')
        import_config_dire(fmtpath(self.base_path,'/configs'))

    @set_triggers('project.impoort.structures')
    def __init_import_structures(self):
        anl.phase('导入构件')
        self.__env['components'].update(Loader.load_compoents(
            fmtpath(self.base_path,'/structures/components')))
        anl.phase('导入卡片模版')
        self.__env['templates'].update(Loader.load_tempaltes(
            fmtpath(self.base_path,'/structures/templates')))
        anl.phase('导入页面模版')
        self.__env['page_templates'].update(Loader.load_page_tempaltes(
            fmtpath(self.base_path,'/structures/pagetemplates')))

    def __init_import_data(self):
        anl.phase('读取数据文件')
        self.__env['data'].update(Loader.create_structure_mapping(
            fmtpath(self.base_path,'/data')))

    @set_triggers('project.import.modules')
    def __init_import_modules(self):
        anl.phase('导入模块')
        logger.info(t('project.import.modules'))
        load_module_dire(fmtpath(self.base_path,'/modules'), self)
        self.__checkModuleWaitList()
    
    @set_triggers('project.import.cards')
    def __init_import_cards(self):
        anl.phase('导入卡片')
        logger.info(t('project.import.cards'))
        self.base_library = Library(File(
            fmtpath(self.base_path,"/Libraries/__LIBRARY__.yml")).data)

    @set_triggers('project.import.resources')
    def __init_import_resources(self):
        anl.phase('导入资源')
        logger.info(t('project.import.resources'))
        self.__env['resources'].update(Loader.load_resources(
            fmtpath(self.base_path,'/resources')))
    
    @set_triggers('project.import.pages')
    def __init_import_pages(self):
        anl.phase('导入页面')
        logger.info(t('project.import.pages'))
        for pagefile in Dire(fmtpath(self.base_path,'/pages')).scan(recur=True):
            self.import_page_from_file(pagefile)

    @set_triggers('project.load')
    def __init__(self,builder, path):
        anl.phase('初始化仓库类')
        logger.info(t('project.init'))
        super().__init__(builder=builder,path=path)
        logger.info(t('project.load.success'))
        anl.pause()

    def import_page_from_file(self, page_file: File):
        """导入页面"""
        file_name = page_file.name
        file_exten = page_file.extention
        if file_exten == 'yml':
            page = CardStackPage(page_file)
            self.__import_card_stack_page(page)
        elif file_exten == 'xaml':
            page = RawXamlPage(page_file)
        else:
            logger.warning(f'Page file not supported: {file_name}.{file_exten}')
            return
        self.pages[file_name] = page
        self.pagelist.append(file_name)

    def __import_card_stack_page(self,page:CardStackPage):
        if page.name:
            self.pages[page.name] = page
        if page.alias:
            for alias in page.alias:
                self.pages[alias] = page

    @set_triggers('project.genxaml')
    def get_page_xaml(self, page_alias, no_not_found_err_logging = False, setter = None):
        """获取页面 xaml 代码"""
        logger.info(t('project.gen_page.start', page=page_alias, args=setter))
        if page_alias not in self.pages:
            if not no_not_found_err_logging:
                logger.error(t('project.gen_page.failed.notfound', page=page_alias))
            raise PageNotFoundError(page_alias)
        env = self.get_environment_copy()
        env.update(setter=setter)
        env.update(used_resources=set())
        xaml = self.pages[page_alias].generate(env = env)
        logger.debug(env.get('used_resources'))
        return xaml

    def get_page_content_type(self, page_alias, no_not_found_err_logging = False, setter = None):
        if page_alias not in self.pages:
            if not no_not_found_err_logging:
                logger.error(t('project.gen_page.failed.notfound', page=page_alias))
            raise PageNotFoundError(page_alias)
        return self.pages[page_alias].get_content_type(setter = setter)
    
    def get_page_displayname(self, page_alias):
        """获取页面显示名"""
        page = self.pages.get(page_alias)
        if not page:
            raise PageNotFoundError(t('page.not_found',page = page_alias))
        return page.display_name

    def set_env_data(self,key,value):
        self.__env['data'][key] = value
    
    def get_env_data(self,key):
        return self.__env['data'].get(key)
class PageNotFoundError(Exception):
    """页面未找到错误"""
