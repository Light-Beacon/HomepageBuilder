import re
import sys
import os
from pathlib import Path
from typing import List, Union, TypeVar, Tuple, Any
from ..logger import Logger
from ..config import config, is_debugging
from .accessor import read

T = TypeVar('T')

logger = Logger('IO')
ANYPATTERN = re.compile('.*')

#region [CONFIG FUNCTIONS]配置文件函数
def IS_ENABLE_SYMLINK() -> bool:
    """是否忽略符号链接"""
    return config('IO.EnableSymbolink',  default=False, except_type=bool)

def IS_ENABLE_SYMLINK_ERROR() -> bool:
    """当遇到符号链接时是否报错"""
    return config('IO.EnableSymbolinkError', default=True, except_type=bool)

def IS_ENABLE_INGORE() -> bool:
    """是否启用文件首尾为特定格式时忽略"""
    return config('IO.EnableIngore', default=False, except_type=bool)

def GET_INGORE_PREFIX() -> List[str]:
    """需要忽略的文件的前缀名"""
    return config('IO.IngorePrefix', default=['#','.'], except_type=list)

def GET_INGORE_SUFFIX() -> List[str]:
    """需要忽略的文件的前缀名"""
    return config('IO.IngoreSuffix', default=['.disabled'], except_type=list)
#endregion

#region [EXCEPTIONS]异常
class SymbolLinkError(Exception):
    '''Target is a symbol link'''

class IsAFileError(Exception):
    '''Operation dosen't work on files'''
#endregion

class File():
    def __init__(self,abs_path:Union[Path, str],read_init = False):
        if isinstance(abs_path, str):
            abs_path = Path(abs_path)
        self.abs_path:Path = abs_path
        self.fullname:str = abs_path.name
        self.direname:Path = abs_path.parent
        self.name,self.extention = os.path.splitext(self.fullname)
        self.extention = self.extention.removeprefix('.')
        self.cache = None
        if read_init:
            self.read()

    def __str__(self):
        return f"File({self.fullname})"

    @property
    def data(self,func = None):
        '''文件数据'''
        #logger.debug(f'读取{self.abs_path}')
        return self.read(func)

    def read(self,func = None,usecache:bool = True, 
             except_type: Union[type[T],Tuple[type[T], ...], Any] = Any, ) -> Union[T, Any]:
        '''读取文件'''
        #logger.debug(f'读取{self.abs_path}')
        if config('Debug.Enable'):
            result = read(self,func,usecache)
        try:
            result = read(self,func,usecache)
        except Exception as ex:
            if is_debugging():
                raise ex
            else:
                logger.warning(ex)
                result = None
        if except_type is not Any and not isinstance(result, except_type):
            if isinstance(except_type, type):
                raise TypeError(f'File {self.abs_path} is not of type {except_type.__name__}')
            elif isinstance(except_type, tuple):
                raise TypeError(f'File {self.abs_path} is not one of those types {",".join([t.__name__ for t in except_type])}')
            else:
                raise TypeError(f'File {self.abs_path} is not of type {except_type}')
        return result
    

    def write(self,*args,func = None,**kwargs):
        '''写入文件'''
        return read(self,*args,func,**kwargs)

class Dire():
    def __init__(self,abs_path:Union[Path, str]):
        if isinstance(abs_path, str):
            abs_path = Path(abs_path)
        if not abs_path.exists():
            raise FileNotFoundError(f'{abs_path} not exist')
        if not abs_path.is_dir():
            raise IsAFileError(f'{abs_path} is a file')
        self.abs_path:Path = abs_path
        self.files:dict[str,File] = {}
        self.dires:dict[str,'Dire'] = {}
        self.name:str = abs_path.name
        self.files:dict[str,File] = {}
        self.dires:dict[str,'Dire'] = {}
        self.__self_scan()

    def __add_node(self,path:Path) -> None:
        basename = path.name
        if path.is_file():
            self.files[basename] = File(path)
        elif path.is_dir():
            self.dires[basename] = Dire(path)
        elif path.is_symlink():
            if IS_ENABLE_SYMLINK():
                self.__add_node(path.readlink())
            elif IS_ENABLE_SYMLINK_ERROR():
                raise SymbolLinkError(f'{path} is a symbol link')
        else:
            raise NotImplementedError(f'Cannot judge type of {path}, it is not a file, directory, or a symbol link.')

    def __should_be_ignored(self, path:Path):
        name = path.name
        for prefix in GET_INGORE_PREFIX():
            if name.startswith(prefix):
                return True
        for suffix in GET_INGORE_SUFFIX():
            if name.endswith(suffix):
                return True
        return False

    def __self_scan(self):
        self.files = {}
        self.dires = {}
        for rel_path in self.abs_path.iterdir():
            if IS_ENABLE_INGORE():
                if self.__should_be_ignored(rel_path):
                    continue
            self.__add_node(self.abs_path/rel_path)

    def scan_subdir(self,patten:Union[str, re.Pattern] = ANYPATTERN):
        '''和 `scan` 效果相似，函数会返回该文件夹所有下边的一层文件夹的指定文件列表'''
        return self.scan(patten=patten,recur=True,min_recur_deepth=1,max_recur_deepth=1)

    def scan(self,
            patten:Union[str, re.Pattern, None] = ANYPATTERN,
            recur:bool=False,
            dire_patten:Union[str, re.Pattern] = ANYPATTERN,
            min_recur_deepth:int = 0,
            max_recur_deepth:int = sys.maxsize,
            include_dires:bool = False,
            include_files:bool = True,
         ) -> List[File]:
        '''遍历文件夹下所有文件夹所有文件, 读取其中符合正则表达式的文件, 最后以列表形式输出
        ## 参数
        ### 常规
            * `[patten]` 文件需要满足的正则，默认 `".*"`
            * `[include_dires]` 指示递归遍历时输出是否包含子文件夹，默认为 `false`
            * `[include_files]` 指示递归遍历时输出是否包含子文件，默认为 `true`
            * `[dire_patten]` 文件夹需要满足的正则，默认 `".*"`
        ### 递归模式
            * `[recur]` 指示是否递归子文件夹，默认 `False`
            * `[min_recur_deepth]` 遍历的最小深度，默认为 `0`
            * `[max_recur_deepth]` 遍历的最大深度，默认为 `sys.maxsize`
        '''
        if not (self.files or self.dires):
            self.__self_scan()
        if not patten:
            patten = ANYPATTERN
        output = []
        if min_recur_deepth <= 0 :
            if include_files:
                for filename in self.files:
                    if re.match(patten,filename):
                        output.append(self.files[filename])
            if include_dires:
                for direname in self.dires:
                    if re.match(dire_patten,direname):
                        output.append(self.dires[direname])
        if recur:
            for direname in self.dires:
                if re.match(dire_patten,direname)\
                and max_recur_deepth > 0:
                    output.extend(self.dires[direname].scan(
                        patten=patten,recur=recur,dire_patten=dire_patten,
                        min_recur_deepth = min_recur_deepth - 1,
                        max_recur_deepth = max_recur_deepth - 1,
                        include_dires = include_dires,include_files=include_files
                    ))
        return output
