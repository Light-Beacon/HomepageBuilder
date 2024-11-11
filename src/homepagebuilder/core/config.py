import os
import yaml

__CONFIG_DICT = {}
FORCE_DEBUGGING = False
SUBSCRIBE_DEBUG_CHANGING_LIST = []

def config(key:str,default = None) -> object:
    """获取配置"""
    return __CONFIG_DICT.get(key,default)

class DisabledByConfig(Exception):
    """被配置禁用"""

def is_debugging() -> bool:
    """在调试模式状态下"""
    return FORCE_DEBUGGING or config('Debug.Enable')

def enable_by_config(key:str,default_output=None,
                     raise_error=False):
    """当配置为 True 时启用的修饰器"""
    def enable_by_config_deco(func:callable):
        def wrapper(*args,**kwagrs):
            if config(key):
                return func(*args,**kwagrs)
            else:
                if raise_error:
                    raise DisabledByConfig()
                else:
                    return lambda *args,**kwagrs: default_output
        return wrapper
    return enable_by_config_deco


def __init_default() -> None:
    """加载默认配置"""
    from .utils.paths import getbuilderpath
    filepath = getbuilderpath('resources/configs/default.yml')
    if not os.path.exists(filepath):
        raise FileNotFoundError(f'Config file {filepath} not exist! Please re-install the program')
    with open(filepath,encoding='utf-8') as f:
        data:dict = yaml.load(f,Loader=yaml.FullLoader)
    __CONFIG_DICT.update(data)

def init_full() -> None:
    """加载所有配置"""
    from .utils.paths import getbuilderpath
    import_config_dire(getbuilderpath("resources/configs"))

def import_config_dire(direpath) -> None:
    """从文件夹路径加载配置"""
    from .io.structure import Dire
    files = Dire(direpath).scan(recur=True,patten=r'.*\.yml')
    for file in files:
        __CONFIG_DICT.update(file.data)

def subscribe_debug_changing(func):
    SUBSCRIBE_DEBUG_CHANGING_LIST.append(func)

def trigger_debug_changing():
    for func in SUBSCRIBE_DEBUG_CHANGING_LIST:
        func()

def force_debug() -> None:
    print('DEBUGMODE ON')
    global FORCE_DEBUGGING
    FORCE_DEBUGGING = True
    trigger_debug_changing()

##ON IMPORTED
__init_default()
