'''
资源结构模块
'''
import re
from os.path import sep
from .IO import Dire
from .logger import Logger
from .module_manager import storge_temp_scripts
from .i18n import locale as t
from .i18n import append_locale
from Debug.timer import count_time

logger = Logger('Resource')
YML_PATTERN = re.compile(r'.*\.yml$')
XAML_PATTERN = re.compile(r'.*\.xaml$')
PY_PATTERN = re.compile(r'.*\.py$')

class Resource:
    '''资源类'''
    def load_resources(self,path:str):
        '''加载资源'''
        logger.info(t('resource.load',path=path))
        self.animations.update(create_res_mapping(f'{path}{sep}Animations',XAML_PATTERN))
        self.components.update(create_res_mapping(f'{path}{sep}Components',XAML_PATTERN))
        self.data.update(create_res_mapping(f'{path}{sep}Data'))
        self.templates.update(create_res_mapping(f'{path}{sep}Templates',YML_PATTERN))
        self.page_templates.update(create_res_mapping(f'{path}{sep}Page_Templates',XAML_PATTERN))
        self.load_scripts(path=path)
        self.styles.update(create_res_mapping(f'{path}{sep}Styles',XAML_PATTERN))
        self.styles.update(create_res_mapping(f'{path}{sep}Styles',YML_PATTERN))
        append_locale(f'{path}{sep}i18n')
        self.components.update({'':''}) # IF Failed return a null component

   #@count_time
    def load_scripts(self,path):
        self.scripts.update(create_res_mapping(f'{path}{sep}Scripts',PY_PATTERN))
        storge_temp_scripts(self.scripts)

    def __init__(self):
        self.animations = {}
        self.components = {}
        self.styles = {}
        self.data = {'global':{}}
        self.scripts = {}
        self.templates = {}
        self.page_templates = {}

def create_res_mapping(path:str,patten = None):
    output = {}
    try:
        dire = Dire(path)
        if patten:
            files = dire.scan(patten)
        else:
            files = dire.scan()
    except FileNotFoundError:
        return output
    except Exception as ex:
        logger.error(ex)
        return
    for file in files:
        output[file.name] = file.data
    return output
