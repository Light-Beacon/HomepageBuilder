from argparse import HelpFormatter
import locale as pylocale
from string import Template
from typing import Annotated
from .config import config
from .logger import Logger
from .io import Dire
from .utils.paths import getbuilderpath

CONFIG_LANG = config('System.Language')

DEFAULT_LANGUAGE, _ = pylocale.getlocale() if str(CONFIG_LANG).lower() == 'auto' else (CONFIG_LANG, None)
if not isinstance(DEFAULT_LANGUAGE, str) or len(DEFAULT_LANGUAGE) == 0:
    DEFAULT_LANGUAGE = 'en_US'

Language = Annotated[str, '语言代码']
TranslationKey = Annotated[str, '翻译键']

locales: dict[Language, dict[TranslationKey, str]] = {}

logger = Logger('i18n')

def init(locales_tree):
    '''初始化'''
    i18n_dire = Dire(getbuilderpath("resources/i18n",))
    files = i18n_dire.scan()
    for file in files:
        locales_tree[file.name] = file.data

def set_default_language(lang_key:str):
    global DEFAULT_LANGUAGE
    DEFAULT_LANGUAGE = lang_key

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

def locale(key:TranslationKey, *args, lang:Language=None, **kwargs):
    """从键值获取字符串"""
    if not lang:
        lang = DEFAULT_LANGUAGE
    language_dict = locales.get(lang)
    if language_dict:
        string = language_dict.get(key)
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
