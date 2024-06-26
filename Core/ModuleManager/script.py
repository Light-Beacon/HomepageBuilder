from typing import Dict
from Core.config import config
from Core.logger import Logger
from Core.i18n import locale as t

logger = Logger('ScriptsManager')
NO_ERR_OUTPUT_WHILE_SCRIPT_NOTFOUND = config('System.Script.IgnoreError')
scripts = {}

def script(script_name):
    '''(修饰器)注册该函数为脚本'''
    def decorator(func):
        scripts[script_name] = func
        return func
    return decorator

def invoke_script(script_name:str,project,card:Dict[str,object],
              args:list,children_code:str):
    '''获取脚本输出结果'''
    resources = project.resources
    if script_name == 'ChildrenPresenter':
        return children_code
    script_code = scripts.get(script_name)
    if script_code is None:
        if NO_ERR_OUTPUT_WHILE_SCRIPT_NOTFOUND:
            logger.warning(t('script.invoke.failed.notfound',name = script_name))
        else:
            logger.error(t('script.invoke.failed.notfound',name = script_name))
        return ''
    result = scripts[script_name](*args,card=card,res=resources,proj=project)
    return result