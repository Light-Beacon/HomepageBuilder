from typing import Dict, TYPE_CHECKING
from ..config import config
from ..logger import Logger
from ..i18n import locale as t

if TYPE_CHECKING:
    from Core.types import BuildingEnvironment

logger = Logger('ScriptsManager')
NO_ERR_OUTPUT_WHILE_SCRIPT_NOTFOUND = config('System.Script.IgnoreError')
scripts = {}

def script(script_name):
    '''(修饰器)注册该函数为脚本
    ## 传入参数
    *args 脚本参数
    card 卡片
    env 环境
    '''
    def decorator(func):
        scripts[script_name] = func
        return func
    return decorator

def invoke_script(script_name:str,env:'BuildingEnvironment',card:Dict[str,object],
              args:list,**kwargs):
    '''获取脚本输出结果'''
    script_code = scripts.get(script_name)
    if script_code is None:
        if NO_ERR_OUTPUT_WHILE_SCRIPT_NOTFOUND:
            logger.warning(t('script.invoke.failed.notfound',name = script_name))
        else:
            logger.error(t('script.invoke.failed.notfound',name = script_name))
        return ''
    result = scripts[script_name](*args,card=card,env=env,**kwargs)
    return result
