'''
文件IO模块
'''
from typing import List,Tuple,Dict,Union
import os
import json
import yaml
from Core.logger import Logger

logger = Logger('IO')

def read_string(filepath:str):
    '''读取字符串文件'''
    with open(filepath, "r+",encoding="utf-8") as file:
        return file.read()

def write_string(filepath:str,data:str):
    '''写入字符串文件'''
    with open(filepath, "w",encoding="utf-8") as file:
        return file.write(data)

def read_json(filepath) -> dict:
    ''' 读取 Json 文件 '''
    if not os.path.exists(filepath):
        raise FileNotFoundError(f'{filepath} not exist!')
    with open(filepath,encoding='utf-8') as f:
        data = json.load(f)
        return data

def read_yaml(filepath:str) -> dict:
    ''' 读取 Yaml 文件 '''
    if not os.path.exists(filepath):
        raise FileNotFoundError(f'{filepath} not exist!')
    with open(filepath,encoding='utf-8') as f:
        data = yaml.load(f,Loader=yaml.FullLoader)
        if data is None:
            data = {}
        data.update({'file_path':filepath})
        return data

def read_python(filepath:str) -> callable:
    ''' 读取 Python 文件 '''
    from Core.module_manager import reg_script
    if not os.path.exists(filepath):
        raise FileNotFoundError(f'{filepath} not exist!')
    return reg_script(filepath)


read_func_mapping = {
    'yml':read_yaml,
    'yaml':read_yaml,
    'json':read_json,
    'py':read_python,
    'python':read_python,
}

def read(file,func = None,usecache:bool = True):
    '''读取文件'''
    if not func:
        if usecache and file.data:
            return file.data
        if file.extention in read_func_mapping:
            func = read_func_mapping[file.extention]
        else:
            func = read_string
        file.data = func(file.abs_path)
        return file.data
    return func(file.abs_path)

def regist_fileread_function(func:callable,file_extens:str) -> None:
    '''注册读取后缀名为 `file_extens` 的文件的函数'''
    def reg_fileread(func,file_exten:str):
        read_func_mapping[file_exten] = func
    if isinstance(file_extens,list):
        for exten in file_extens:
            reg_fileread(func,exten)
    elif isinstance(file_extens,str):
        reg_fileread(func,file_extens)
    else:
        raise TypeError()
