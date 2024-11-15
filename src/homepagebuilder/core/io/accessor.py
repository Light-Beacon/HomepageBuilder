import os
from ..logger import Logger
from typing import Iterable
logger = Logger('IO')

read_func_mapping = {}
write_func_mapping = {}

class FileFormatUnsupportedError(Exception):
    def __init__(self,file, *args: object) -> None:
        from ..i18n import locale
        super().__init__(*args)
        self.file = file
        self.msg = locale('io.format.unsupported',path=file.abs_path,exten = file.extention)
    
    def __str__(self):
        return self.msg

def regist_file_function(func:callable,action:str,file_extentions:str) -> None:
    '''注册后缀名为 `file_extens` 的文件的读写函数'''
    def reg_filetype(func,file_exten:str,action:str):
        if action == 'r':
            read_func_mapping[file_exten] = func
        elif action == 'w':
            write_func_mapping[file_exten] = func
    if isinstance(file_extentions,str):
        if file_extentions[0] == '.':
            file_extentions = file_extentions[1:]
        reg_filetype(func,file_extentions,action)
    elif isinstance(file_extentions,Iterable):
        for exten in file_extentions:
            regist_file_function(func,action,exten)
    else:
        raise TypeError()

def file_reader(*file_extentions):
    '''(修饰器)注册该函数为文件读取函数'''
    def decorator(func):
        regist_file_function(func,'r',file_extentions)
        return func
    return decorator

def file_writer(*file_extentions):
    '''(修饰器)注册该函数为文件写入函数'''
    def decorator(func):
        regist_file_function(func,'w',file_extentions)
        return func
    return decorator

def read(file,func = None,usecache:bool = True):
    '''读取文件'''
    if not os.path.exists(file.abs_path):
        raise FileNotFoundError(f'{file.abs_path} not exist!')
    if not func:
        if usecache and file.cache:
            return file.cache
        if file.extention in read_func_mapping:
            func = read_func_mapping[file.extention]
        else:
            raise FileFormatUnsupportedError(file)
        file.cache = func(file.abs_path)
        return file.cache
    return func(file.abs_path)

def write(file,*arg,func = None,**kwarg):
    '''写入文件'''
    if not func:
        if file.extention in write_func_mapping:
            func = write_func_mapping[file.extention]
        else:
            func = write_func_mapping['txt']
        return file.data
    return func(file.abs_path,*arg,**kwarg)
