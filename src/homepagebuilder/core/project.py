"""
工程文件模块，构建器核心
"""
import os
from typing import TYPE_CHECKING
from .io import Dire, File
from .library import Library
from .logger import Logger
from .i18n import locale as t
from .module_manager import load_module_dire,get_check_list
from .utils.event import set_triggers
from .utils.paths import fmtpath
from .utils.checking import Version
from .utils.client import DEFAULT_PCLCLIENT
from .page import CardStackPage, RawXamlPage
from .loader import Loader
from .types import Project as ProjectBase
from .config import import_config_dire

if TYPE_CHECKING:
    from .utils.client import PCLClient
    
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
        logger.info(t('project.import.start', path=path))
        self.__init_load_projectfile(path)
        self.__init_import_configs()
        self.__init_import_modules()
        self.__init_import_structures()
        self.__init_import_resources()
        self.__init_import_cards()
        self.__init_import_pages()
        self.__init_import_data()
        logger.info(t('project.import.success'))

    @set_triggers('project.import.projectfile')
    def __init_load_projectfile(self,path):
        pack_info = File(path).read()
        self.base_path = os.path.dirname(path)
        self.version = Version.from_string(pack_info['version'])
        self.default_page = pack_info.get('default_page')
        self.__check_version()

    def __check_version(self):
        builder_version = Version.builder_version()
        pack_version = self.version
        if pack_version >> builder_version:
            logger.warning(t('project.import.pack.version.too.new',
                             packversion = pack_version,builderversion = builder_version))
        elif pack_version << builder_version:
            logger.warning(t('project.import.pack.version.too.old',
                             packversion = pack_version,builderversion = builder_version))
        elif pack_version > builder_version:
            logger.info(t('project.import.pack.version.new',
                          packversion = pack_version,builderversion = builder_version))
        elif pack_version < builder_version:
            logger.info(t('project.import.pack.version.old',
                          packversion = pack_version,builderversion = builder_version))
        else:
            logger.info(t('project.import.pack.version', packversion=self.version))

    def __init_import_configs(self):
        try:
            import_config_dire(fmtpath(self.base_path,'/configs'))
        except FileNotFoundError:
            pass

    @set_triggers('project.impoort.structures')
    def __init_import_structures(self):
        self.__context.components.update(Loader.load_compoents(
            fmtpath(self.base_path,'/structures/components')))
        self.__context.templates.update(Loader.load_tempaltes(
            fmtpath(self.base_path,'/structures/templates')))
        self.__context.page_templates.update(Loader.load_page_tempaltes(
            fmtpath(self.base_path,'/structures/pagetemplates')))

    def __init_import_data(self):
        self.__context.data.update(Loader.create_structure_mapping(
            fmtpath(self.base_path,'/data')))

    @set_triggers('project.import.modules')
    def __init_import_modules(self):
        logger.info(t('project.import.modules'))
        load_module_dire(fmtpath(self.base_path,'/modules'), self)
        self.__checkModuleWaitList()

    @set_triggers('project.import.cards')
    def __init_import_cards(self):
        logger.info(t('project.import.cards'))
        self.base_library = Library(File(
            fmtpath(self.base_path,"/libraries/__LIBRARY__.yml")).data)

    @set_triggers('project.import.resources')
    def __init_import_resources(self):
        logger.info(t('project.import.resources'))
        self.__context.resources.update(Loader.load_resources(
            fmtpath(self.base_path,'/resources')))

    @set_triggers('project.import.pages')
    def __init_import_pages(self):
        logger.info(t('project.import.pages'))
        for pagefile in Dire(fmtpath(self.base_path,'/pages')).scan(recur=True):
            self.import_page_from_file(pagefile)

    @set_triggers('project.load')
    def __init__(self,builder, path):
        logger.info(t('project.init'))
        super().__init__(builder=builder,path=path)
        logger.info(t('project.load.success'))

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
    def find_page_by_alias(self, page_alias, no_not_found_err_logging = False):
        """从别名获取页面对象"""
        if page_alias not in self.pages:
            if not no_not_found_err_logging:
                logger.error(t('project.gen_page.failed.notfound', page=page_alias))
            raise PageNotFoundError(page_alias)
        return self.pages[page_alias]

    @set_triggers('project.genxaml')
    def get_page_xaml(self, page_alias, no_not_found_err_logging = False, setter = None, client = DEFAULT_PCLCLIENT):
        """使用页面别名获取其 xaml 代码"""
        logger.info(t('project.gen_page.start', page=page_alias, args=setter))
        page = self.find_page_by_alias(page_alias, no_not_found_err_logging)
        return self.generate_page_xaml(page, setter, client)

    def generate_page_xaml(self, page, setter = None, client = DEFAULT_PCLCLIENT):
        """使用页面对象生成 xaml 代码"""
        context = self.get_context_copy()
        context.setter = setter
        context.client = client
        context.used_resources = set()
        return page.generate(context = context)

    def get_page_content_type(self, page_alias, no_not_found_err_logging = False, setter = None, client:'PCLClient' = DEFAULT_PCLCLIENT):
        if page_alias not in self.pages:
            if not no_not_found_err_logging:
                logger.error(t('project.gen_page.failed.notfound', page=page_alias))
            raise PageNotFoundError(page_alias)
        return self.pages[page_alias].get_content_type(setter = setter, client = client)

    def get_page_displayname(self, page_alias):
        """获取页面显示名"""
        page = self.pages.get(page_alias)
        if not page:
            raise PageNotFoundError(t('page.not_found', page = page_alias))
        return page.display_name

    def set_context_data(self,key,value):
        self.__context.data[key] = value
    
    def get_context_data(self,key):
        return self.__context.data.get(key)
class PageNotFoundError(Exception):
    """页面未找到错误"""
