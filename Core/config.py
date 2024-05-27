import os
import yaml

config_dict = {}
def config(key):
    return config_dict.get(key)

def __init__():
    global config_dict
    envpath = os.path.dirname(os.path.dirname(__file__))
    filepath = f"{envpath}{os.path.sep}Config{os.path.sep}basic.yml"
    if not os.path.exists(filepath):
        raise FileNotFoundError(f'Config file {filepath} not exist! Please re-install the program')
    with open(filepath,encoding='utf-8') as f:
        data:dict = yaml.load(f,Loader=yaml.FullLoader)
    config_dict = data

__init__()
