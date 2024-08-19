'''
资源结构模块
'''
import re
from os.path import sep
from .IO import Dire,File
from .logger import Logger
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
        #self.load_scripts(path=path)
        self.styles.update(create_res_mapping(f'{path}{sep}Styles',XAML_PATTERN))
        self.styles.update(create_res_mapping(f'{path}{sep}Styles',YML_PATTERN))
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

def create_res_mapping(path:str,patten = None):
    output = {}
    try:
        dire = Dire(path)
        mapping_file(dire,output,'',patten)
    except FileNotFoundError:
        return output
    except Exception as ex:
        logger.error(ex)
        return
    return output

def mapping_file(file_or_dire,output,prefix = '',patten = None,is_toplevel:bool = True):
    if isinstance(file_or_dire,File):
        file = file_or_dire
        output[prefix + file.name] = file.data
    elif isinstance(file_or_dire,Dire):
        dire = file_or_dire
        for node in dire.scan(patten,include_dires=True):
            mapping_file(node,output,patten=patten,is_toplevel = False,
                         prefix = '' if is_toplevel else f'{prefix}{dire.name}/')
    else:
        raise TypeError()
