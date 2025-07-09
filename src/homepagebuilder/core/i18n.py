from argparse import HelpFormatter
from locale import getdefaultlocale
from string import Template
from .config import config
from .logger import Logger
from .io import Dire
from .utils.paths import getbuilderpath
CONFIG_LANG = config('System.Language')
DEFAULTLANG,_  = getdefaultlocale() if str(CONFIG_LANG).lower() == 'auto' else (CONFIG_LANG,None)
locales = {}
logger = Logger('i18n')

def init(locales_tree):
    '''初始化'''
    i18n_dire = Dire(getbuilderpath("resources/i18n",))
    files = i18n_dire.scan()
    for file in files:
        locales_tree[file.name] = file.data

def append_locale(path):
    '''加载更多本地化包'''
    locales_tree = locales
    try:
        dire = Dire(path)
    except FileNotFoundError:
        return
    except Exception as ex:
        logger.error(ex)
        return
    files = dire.scan()
    for file in files:
        lang = file.name
        if lang in locales_tree:
            locales_tree[lang].update(file.data)
        else:
            locales_tree[lang] = file.data

def locale(key:str,*args,lang:str=DEFAULTLANG,**kwargs):
    '''从键值获取字符串'''
    if lang in locales:
        string = locales.get(lang).get(key)
        if not string:
            if lang != 'en_US':
                string = locale(key,lang='en_US',*args,**kwargs)
            else:
                string = key
        try:
            result = Template(string).substitute(*args,**kwargs)
            return result
        except KeyError:
            return f"{key}: {args} {kwargs}"
    else:
        return locale(key,lang='en_US',**kwargs)

init(locales)

class LocalizedHelpFormatter(HelpFormatter):
    """本地化帮助格式化器"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = locale('command.usage_prefix')
        return super().add_usage(usage, actions, groups, prefix)

    def start_section(self, heading):
        translations = {
            'positional arguments': 'command.positional_arguments',
            'optional arguments': 'command.optional_arguments',
            'options': 'command.options',
        }
        if heading in translations:
            heading = locale(translations[heading])
        super().start_section(heading)
