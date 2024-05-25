import os
from locale import getlocale as get_sys_locale
from string import Template
from .io import scan_dire, try_scan_dire
locales = {}
syslang,_  = get_sys_locale()

def init(locales_tree):
    '''初始化'''
    envpath = os.path.dirname(os.path.dirname(__file__))
    file_infos = scan_dire(f"{envpath}{os.path.sep}i18n",)
    for data,lang,_ in file_infos:
        locales_tree[lang] = data

def append_locale(path):
    '''加载更多本地化包'''
    locales_tree = locales
    file_infos = try_scan_dire(path)
    for data,lang,_ in file_infos:
        if lang in locales_tree:
            locales_tree[lang].update(data)
        else:
            locales_tree[lang] = data

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
