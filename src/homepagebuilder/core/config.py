import os
import yaml
from typing import TypeVar, Union, Tuple, Any, Callable

T = TypeVar('T')

__CONFIG_DICT = {}
FORCE_DEBUGGING = False

CONFIG_CHANGE_EVENT_SUBSCRIBERS = {}
def on_config_changing(*config_keys: str):
    """[装饰器]订阅配置改变事件"""
    def wrapper(func):
        for config_key in config_keys:
            if config_key not in CONFIG_CHANGE_EVENT_SUBSCRIBERS:
                CONFIG_CHANGE_EVENT_SUBSCRIBERS[config_key] = []
            CONFIG_CHANGE_EVENT_SUBSCRIBERS[config_key].append(func)
        return func
    return wrapper

def __trigger_congfig_changing(config_key:str):
    """触发配置改变事件"""
    if subscribers := CONFIG_CHANGE_EVENT_SUBSCRIBERS.get(config_key):
        for func in subscribers:
            func()

def config(key:str, default = None, except_type: Union[type[T],Tuple[type[T], ...], Any] = Any, ) -> Union[T, Any]:
    """获取配置"""
    value = __CONFIG_DICT.get(key,default)
    if except_type is not Any and not isinstance(value, except_type):
        if isinstance(except_type, type):
            raise TypeError(f'Config {key} is not of type {except_type.__name__}')
        elif isinstance(except_type, tuple):
            raise TypeError(f'Config {key} is not one of those types {",".join([t.__name__ for t in except_type])}')
        else:
            raise TypeError(f'Config {key} is not of type {except_type}')
    return value

def set_config(key:str,value:object) -> None:
    """设置配置"""
    __CONFIG_DICT[key] = value
    __trigger_congfig_changing(key)

class DisabledByConfig(Exception):
    """被配置禁用"""

def is_debugging() -> bool:
    """在调试模式状态下"""
    return config('Debug.Enable')

def enable_by_config(key:str,default_output=None,
                     raise_error=False):
    """当配置为 True 时启用的修饰器"""
    def enable_by_config_deco(func:Callable):
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
    for key in data:
        __trigger_congfig_changing(key)

def init_full() -> None:
    """加载所有配置"""
    from .utils.paths import getbuilderpath
    import_config_dire(getbuilderpath("resources/configs"))

def import_config_dire(direpath) -> None:
    """从文件夹路径加载配置"""
    from .io.structure import Dire
    files = Dire(direpath).scan(recur=True,patten=r'.*\.yml')
    for file in files:
        if not isinstance(file.data, dict):
            raise TypeError(f'Config file {file.abs_path} is not a dict!')
        __CONFIG_DICT.update(file.data)
        for key in file.data:
            __trigger_congfig_changing(key)

def force_debug() -> None:
    print('DEBUGMODE ON')
    set_config('Debug.Enable', True)

##ON IMPORTED
__init_default()
