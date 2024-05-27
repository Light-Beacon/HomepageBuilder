import os
import yaml

config_dict = {}
def config(key):
    return config_dict.get(key)

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
    from .IO import Dire
    files = Dire(os.path.dirname(os.path.dirname(__file__))).scan(recur=True,patten=r'.*\.yml')
    for file in files:
        config_dict.update(file.read())

partly_init()
