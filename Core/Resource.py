'''
资源结构模块
'''
from os.path import sep
from .io import create_dict,try_scan_dire
from .debug import Logger
from .module_manager import storge_temp_scripts
from .i18n import locale as t
from .i18n import append_locale

logger = Logger('Resource')
class Resource:
    '''资源类'''
    def load_resources(self,path:str,prefix:str):
        '''加载资源'''
        logger.info(t('resource.load',path=path))
        self.animations.update(create_dict(try_scan_dire(
            f'{path}{sep}Animations',r'.*\.xaml$'),prefix))
        self.components.update(create_dict(try_scan_dire(
            f'{path}{sep}Components',r'.*\.xaml$'),prefix))
        self.templates.update(create_dict(try_scan_dire(
            f'{path}{sep}Templates',r'.*\.yml$'),prefix))
        self.data.update(create_dict(try_scan_dire(
            f'{path}{sep}Data',r'.*'),prefix))
        self.templates.update(create_dict(try_scan_dire(
            f'{path}{sep}Templates',r'.*\.yml$'),prefix))
        self.page_templates.update(create_dict(try_scan_dire(
            f'{path}{sep}Page_Templates',r'.*\.xaml$'),prefix))
        self.scripts.update(create_dict(try_scan_dire(
            f'{path}{sep}Scripts',r'.*\.py$'),prefix))
        storge_temp_scripts(self.scripts)
        self.styles.update(create_dict(try_scan_dire(
            f'{path}{sep}Styles',r'.*\.xaml$'),prefix))
        self.styles.update(create_dict(try_scan_dire(
            f'{path}{sep}Styles',r'.*\.yml$'),prefix))
        append_locale(f'{path}{sep}i18n')
        self.components.update({'':''}) # IF Failed return a null component

    def __init__(self):
        self.animations = {}
        self.components = {}
        self.styles = {}
        self.data = {'global':{}}
        self.scripts = {}
        self.templates = {}
        self.page_templates = {}
