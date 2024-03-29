import yaml
import json
import os
import re
import importlib
import sys
from typing import List,Tuple,Dict
from .Debug import LogInfo

def readString(filepath:str):
    # 读取字符串文件
    with open(filepath, "r+",encoding="utf-8") as file:
        return file.read()
    
def writeString(filepath:str,data:str):
    '''写入字符串文件'''
    with open(filepath, "w") as file:
        return file.write(data)

def readJson(filepath) -> dict:
    ''' 读取 Json 文件 '''
    if not os.path.exists(filepath):
        raise FileNotFoundError(f'{filepath} not exist!')
    with open(filepath,encoding='utf-8') as f:
        data = json.load(f)
        return data
    
def readYaml(filepath) -> dict:
    ''' 读取 Yaml 文件 '''
    if not os.path.exists(filepath):
        raise FileNotFoundError(f'{filepath} not exist!')
    with open(filepath,encoding='utf-8') as f:
        data = yaml.load(f,Loader=yaml.FullLoader)
        if data is None:
            data = {} 
        data.update({'file_path':filepath})
        return data

def readPy(filepath) -> callable:
    ''' 读取 Python 文件 '''
    if not os.path.exists(filepath):
        raise FileNotFoundError(f'{filepath} not exist!')
    path_to = os.path.dirname(filepath)
    file_name = os.path.basename(filepath)
    name,exten = os.path.splitext(file_name)
    sys.path.append(path_to)
    module = importlib.import_module(f'{name}')
    if hasattr(module,'script'):
        func = getattr(module,'script')
        if not callable(func):
            raise Exception(f'{filepath} script not callable')
    else:
        return None
    return func

def regist_fileread_function(func,file_extens):
    def reg_fileread(func,file_exten:str):
        read_func_mapping[file_exten] = func
    if isinstance(file_extens,list):
        for exten in file_extens:
            reg_fileread(func,exten)
    elif isinstance(file_extens,str):
        reg_fileread(func,file_extens)
    else:
        raise TypeError()
    
read_func_mapping = {
    'yml':readYaml,
    'yaml':readYaml,
    'json':readJson,
    'py':readPy,
    'python':readPy
}

def TryScanDire(direpath:str, regex:str, asraw:bool = False):
    try:
        return ScanDire(direpath,regex,asraw)
    except FileNotFoundError:
        return []

def getAllFileInDire(direpath:str, regex:str):
    output: List[str] = []
    if not os.path.exists(direpath):
        raise FileNotFoundError(f'{direpath} not exist!')
    for f in os.listdir(direpath):
        if os.path.isdir(f'{direpath}{os.path.sep}{f}'):
            continue
        if re.match(regex,f):
            output.append(f)
    return output

def ScanDire(direpath:str, regex:str, asraw:bool = False):
    ''' 返回所有目录下所有文件名符合正则表达式的文件，以元组（读取出的信息，文件名，文件名后缀）的列表输出 '''
    output:List[Tuple[object,str,str]] = []
    if not os.path.exists(direpath):
        raise FileNotFoundError(f'{direpath} not exist!')
    # Log(f'[FileIO] ScanDire {direpath}')
    for f in getAllFileInDire(direpath,regex):
        filename, exten = os.path.splitext(f)
        # 为 # 或 . 开头的文件不读取
        if filename.startswith('#') or filename.startswith('.'):
            continue
        f = f'{direpath}{os.path.sep}{f}'
        exten = exten[1:]
        try:
            if asraw or exten not in read_func_mapping:
                output.append((readString(f),filename,exten))
            else:
                output.append((read_func_mapping[exten](f),filename,exten))
        except FileNotFoundError:
            LogInfo(f'[FileIO] Fail to load {f}!')            
    return output

def ScanSubDire(direpath:str, regex:str, 
                asraw:bool = False) -> List[Tuple[object,str,str]]:
    '''遍历文件夹下所有文件夹(不递归打开), 读取其中符合正则表达式的文件, 以 yaml 格式读取各个文件, 最后以元组（读取出的信息，文件名，文件名后缀）的列表形式输出''' 
    # Log(f'[FileIO] ScanSubDire {direpath}')
    output:List = []
    if not os.path.exists(direpath):
        raise FileNotFoundError(f'{direpath} not exist!')
    for entry in os.scandir(direpath):
        if entry.is_dir():
            output += ScanDire(entry.path,regex,asraw)
    return output

def CreateDict(file_tuple_list:List[Tuple[object,str,str]],
               prefix:str) -> Dict[str,object]:
    result = {}
    for tuple in file_tuple_list:
        data,name,ext = tuple
        result.update({(prefix+name):data})
    return result
