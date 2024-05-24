'''
工程文件模块，构建器核心
'''
import os
from .io import read_yaml, scan_dire, scan_sub_dire
from .library import Library
from .resource import Resource
from .styles import get_style_code
from .templates_manager import TemplateManager
from .code_formatter import format_code
from .debug import log_info, log_error, log_warning
from . import module_manager

PATH_SEP = os.path.sep

class Project:
    '''工程类'''
    def load_plugins(self,plugin_path):
        '''加载插件'''
        for data,_,_ in scan_sub_dire(plugin_path,r'pack.yml'):
            dire = os.path.dirname(data['file_path'])
            self.resources.load_resources(f'{dire}{PATH_SEP}Resources','')

    def import_pack(self,path):
        '''导入资源包'''
        log_info(f'[Project] Start to import pack at: {path}')
        pack_info = read_yaml(path)
        self.version = pack_info['version']
        self.default_page = pack_info.get('default_page')
        log_info(f'[Project] Pack version: {self.version}')
        self.base_path = os.path.dirname(path)
        log_info('[Project] Loading cards')
        self.base_library = Library(read_yaml(
            f"{self.base_path}{PATH_SEP}Libraries{PATH_SEP}__LIBRARY__.yml"))
        log_info('[Project] Importing resources')
        self.resources.load_resources(f'{self.base_path}{PATH_SEP}Resources','')
        log_info('[Project] Loading pages')
        for page in scan_dire(f'{self.base_path}{PATH_SEP}Pages',r'.*'):
            self.import_page(page)

    def get_all_card(self) -> list:
        '''获取工程里的全部卡片'''
        return self.base_library.get_all_cards()

    def __init__(self,path):
        log_info('[Project] Initing ...')
        envpath = os.path.dirname(os.path.dirname(__file__))
        self.resources = Resource()
        log_info('[Project] Loading basic resources')
        self.resources.load_resources(f'{envpath}{PATH_SEP}Resources','')
        log_info('[Project] Loading plugins')
        self.load_plugins(f'{envpath}{PATH_SEP}Plugin')
        self.pages = {}
        self.import_pack(path)
        module_manager.storge_temp_scripts(self.resources.scripts)
        module_manager.init_modules(self)
        self.template_manager = TemplateManager(self)
        log_info('[Project] Pack loaded successful!')

    def import_page(self,page_tuple):
        '''导入页面'''
        page, file_name, file_exten = page_tuple
        if file_exten == 'yml':
            if 'name' in page:
                self.pages.update({ page['name']:page })
            self.pages.update({file_name:page})
            if 'alias' in page:
                for alias in page.get('alias'):
                    self.pages.update({alias:page})
        elif file_exten == 'xaml':
            self.pages.update({file_name:{'xaml':page}})
        else:
            log_warning(f'[Project] Page file not supported: {file_name}.{file_exten}')

    def get_card_xaml(self,card_ref):
        '''获取卡片 xaml 代码'''
        card_ref = format_code(code=card_ref,card={},project=self)
        if ';' in card_ref:
            code = ''
            for each_card_ref in card_ref.split(';'):
                code += self.get_card_xaml(each_card_ref)
            return code
        log_info(f'[Project] Get card: {card_ref}')
        card_ref = card_ref.replace(' ','').split('|')
        if card_ref[0] == '':
            return ''
        try:
            card = self.base_library.get_card(card_ref[0],False)
        except Exception as ex:
            log_warning(f'[Project] 获取卡片失败 {ex}')
            return ''
        if len(card_ref) > 1:
            for arg in card_ref[1:]:
                argname,argvalue = arg.split('=')
                card[argname] = argvalue
        card_xaml = self.template_manager.build(card)
        #card_xaml = format_code(card_xaml,card,self.resources.scripts)
        return card_xaml

    def get_page_xaml(self,page_alias):
        '''获取页面 xaml 代码''' 
        log_info(f'[Project] Getting codes of page: {page_alias}')
        if page_alias not in self.pages:
            raise PageNotFoundError(log_error(f'[Project] Cannot find page named "{page_alias}"'))
        content_xaml = ''
        page = self.pages[page_alias]
        if 'xaml' in page:
            return page['xaml']
        for card_ref in page['cards']:
            content_xaml += self.get_card_xaml(card_ref)
        page_xaml = self.resources.page_templates['Default']
        page_xaml = page_xaml.replace('${animations}','') # TODO
        page_xaml = page_xaml.replace('${styles}',get_style_code(self.resources.styles))
        page_xaml = page_xaml.replace('${content}',content_xaml)
        return page_xaml

    def get_page_displayname(self,page_alias):
        '''获取页面显示名'''
        if page_alias not in self.pages:
            raise PageNotFoundError(log_error(f'[Project] Cannot find page named "{page_alias}"'))
        page = self.pages[page_alias]
        if not (result := page.get('display_name')):
            result = page.get('name')
        return result
class PageNotFoundError(Exception):
    '''页面未找到错误'''
