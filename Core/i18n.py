import os
from locale import getlocale as get_sys_locale
from string import Template
from .IO import Dire
from .logger import Logger

locales = {}
syslang,_  = get_sys_locale()
logger = Logger('i18n')

def init(locales_tree):
    '''初始化'''
    envpath = os.path.dirname(os.path.dirname(__file__))
    i18n_dire = Dire(f"{envpath}{os.path.sep}i18n",)
    files = i18n_dire.scan()
    for file in files:
        locales_tree[file.name] = file.read()

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
            locales_tree[lang].update(file.read())
        else:
            locales_tree[lang] = file.read()

def locale(key:str,*args,lang:str=syslang,**kwargs):
    '''从键值获取字符串'''
    if lang in locales:
        string = locales.get(lang).get(key)
        if not string:
            if lang != 'en_US':
                string = locale(key,lang='en_US',*args,**kwargs)
            else:
                string = key
        return Template(string).substitute(*args,**kwargs)
    else:
        return locale(key,lang='en_US')

init(locales)
