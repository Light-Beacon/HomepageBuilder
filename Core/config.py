import os
import yaml

config_dict = {}


def config(key):
    """获取配置"""
    return config_dict.get(key)


class DisabledByConfig(Exception):
    """被配置禁用"""



def enable_by_config(key:str,default_output=None,
                     raise_error=False):
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


def partly_init():
    global config_dict
    envpath = os.path.dirname(os.path.dirname(__file__))
    filepath = f"{envpath}{os.path.sep}Config{os.path.sep}basic.yml"
    if not os.path.exists(filepath):
        raise FileNotFoundError(f'Config file {filepath} not exist! Please re-install the program')
    with open(filepath,encoding='utf-8') as f:
        data:dict = yaml.load(f,Loader=yaml.FullLoader)
    config_dict = data

def fully_init():
    from .IO import Dire,ENVPATH
    files = Dire(f"{ENVPATH}{os.path.sep}i18n",).scan(recur=True,patten=r'.*\.yml')
    for file in files:
        config_dict.update(file.data)

partly_init()
