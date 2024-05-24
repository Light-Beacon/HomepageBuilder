'''
文件IO模块
'''
from typing import List,Tuple,Dict
import os
import json
import re
import yaml
from .debug import log_info
from .module_manager import reg_script

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
    if not os.path.exists(filepath):
        raise FileNotFoundError(f'{filepath} not exist!')
    return reg_script(filepath)

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

read_func_mapping = {
    'yml':read_yaml,
    'yaml':read_yaml,
    'json':read_json,
    'py':read_python,
    'python':read_python
}

def try_scan_dire(direpath:str, regex:str, asraw:bool = False) -> List[Tuple[object,str,str]]:
    '''
    尝试扫描文件夹，与`ScanDire`功能相同，但若文件不存在不会抛出异常
    '''
    try:
        return scan_dire(direpath,regex,asraw)
    except FileNotFoundError:
        return []

def get_all_filenames_in_dire(direpath:str, regex:str) -> List[str]:
    '''获取文件夹内所有文件名'''
    output: List[str] = []
    if not os.path.exists(direpath):
        raise FileNotFoundError(f'{direpath} not exist!')
    for f in os.listdir(direpath):
        if os.path.isdir(f'{direpath}{os.path.sep}{f}'):
            continue
        if re.match(regex,f):
            output.append(f)
    return output

def scan_dire(direpath:str, regex:str, asraw:bool = False) -> List[Tuple[object,str,str]]:
    ''' 返回所有目录下所有文件名符合正则表达式的文件，以元组（读取出的信息，文件名，文件名后缀）的列表输出 '''
    output:List[Tuple[object,str,str]] = []
    if not os.path.exists(direpath):
        raise FileNotFoundError(f'{direpath} not exist!')
    # Log(f'[FileIO] ScanDire {direpath}')
    for f in get_all_filenames_in_dire(direpath,regex):
        filename, exten = os.path.splitext(f)
        # 为 # 或 . 开头的文件不读取
        if filename.startswith('#') or filename.startswith('.'):
            continue
        f = f'{direpath}{os.path.sep}{f}'
        exten = exten[1:]
        try:
            if asraw or exten not in read_func_mapping:
                output.append((read_string(f),filename,exten))
            else:
                output.append((read_func_mapping[exten](f),filename,exten))
        except FileNotFoundError:
            log_info(f'[FileIO] Fail to load {f}!')
    return output

def scan_sub_dire(direpath:str, regex:str,
                asraw:bool = False) -> List[Tuple[object,str,str]]:
    '''遍历文件夹下所有文件夹(不递归打开), 读取其中符合正则表达式的文件, 以 yaml 格式读取各个文件, 最后以元组（读取出的信息，文件名，文件名后缀）的列表形式输出''' 
    # Log(f'[FileIO] ScanSubDire {direpath}')
    output:List = []
    if not os.path.exists(direpath):
        raise FileNotFoundError(f'{direpath} not exist!')
    for entry in os.scandir(direpath):
        if entry.is_dir():
            output += scan_dire(entry.path,regex,asraw)
    return output

def create_dict(file_tuple_list:List[Tuple[object,str,str]],
               prefix:str) -> Dict[str,object]:
    '''创建文件名到文件对象的映射'''
    result = {}
    for data,name,_ in file_tuple_list:
        result.update({(prefix+name):data})
    return result
