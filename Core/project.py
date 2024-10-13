"""
工程文件模块，构建器核心
"""
import os
from .IO import Dire, File
from .library import Library
from .logger import Logger
from .i18n import locale as t
from .config import enable_by_config
from .ModuleManager import load_module_dire,get_check_list
from .utils.event import trigger_invoke,trigger_return,triggers
from Debug import count_time, global_anlyzer as anl
from .page import CardStackPage, RawXamlPage, PageBase
from Core.types import Project as ProjectBase

PATH_SEP = os.path.sep
logger = Logger('Project')

class Project(ProjectBase):
    """工程类"""

    def __checkModuleWaitList(self):
        if len(wait_list := get_check_list()) > 0:
            logger.error(t('project.check_module_list.error', wait_list=wait_list))

    @triggers('project.import')
    def import_pack(self, path):
        """导入工程包"""
        anl.phase('加载工程包')
        anl.switch_in()
        logger.info(t('project.import.start', path=path))
        self.__init_load_projectfile(path)
        self.__init_import_cards()
        self.__init_import_resources()
        self.__init_import_pages()
        self.__init_import_modules()
        anl.switch_out()
        logger.info(t('project.import.success'))

    @triggers('project.import.projectfile')
    def __init_load_projectfile(self,path):
        anl.phase('读取工程文件')
        pack_info = File(path).read()
        self.base_path = os.path.dirname(path)
        self.version = pack_info['version']
        self.default_page = pack_info.get('default_page')
        logger.info(t('project.import.pack.version', version=self.version))

    @triggers('project.import.modules')
    def __init_import_modules(self):
        anl.phase('导入模块')
        logger.info(t('project.import.modules'))
        load_module_dire(f'{self.base_path}{PATH_SEP}Modules', self)
        self.__checkModuleWaitList()
    
    @triggers('project.import.cards')
    def __init_import_cards(self):
        anl.phase('导入卡片')
        logger.info(t('project.import.cards'))
        self.base_library = Library(File(
            f"{self.base_path}{PATH_SEP}Libraries{PATH_SEP}__LIBRARY__.yml").data)

    @triggers('project.import.resources')
    def __init_import_resources(self):
        anl.phase('导入资源')
        logger.info(t('project.import.resources'))
        self.resources.load_resources(f'{self.base_path}{PATH_SEP}Resources')
    
    @triggers('project.import.pages')
    def __init_import_pages(self):
        anl.phase('导入页面')
        logger.info(t('project.import.pages'))
        for pagefile in Dire(f'{self.base_path}{PATH_SEP}Pages').scan(recur=True):
            self.import_page_from_file(pagefile)

    @trigger_invoke('project.loading')
    @trigger_return('project.loaded')
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

    def get_page_xaml(self, page_alias, no_not_found_err_logging = False, setter = None):
        """获取页面 xaml 代码"""
        logger.info(t('project.gen_page.start', page=page_alias, args=setter))
        if page_alias not in self.pages:
            if not no_not_found_err_logging:
                logger.error(t('project.gen_page.failed.notfound', page=page_alias))
            raise PageNotFoundError(page_alias)
        env = self.get_environment_copy()
        env.update(setter=setter)
        return self.pages[page_alias].generate(env = env)

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

class PageNotFoundError(Exception):
    """页面未找到错误"""
