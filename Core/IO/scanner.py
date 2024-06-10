import re
import os
import sys
from typing import List,Dict,Union
from Core.config import config
from Core.logger import Logger
from .reader import read
from .writer import write

logger = Logger('IO')
ALL = re.compile('.*')
SEP = os.path.sep

ENABLE_SYMLINK = config('IO.EnableSymbolink')
ENABLE_SYMLINK_ERROR = config('IO.EnableSymbolinkError')
ENABLE_INGORE = config('IO.EnableIngore')
INGORE_PREFIX = config('IO.IngorePrefix')
INGORE_SUFFIX = config('IO.IngoreSuffix')

class SymbolLinkError(Exception):
    '''Target is a symbol link'''

class IsAFileError(Exception):
    '''Operation dosen't work on files'''

class File():
    def __init__(self,abs_path,read_init = False):
        self.abs_path = abs_path
        self.fullname = os.path.basename(abs_path)
        self.name,self.extention = os.path.splitext(self.fullname)
        self.extention = self.extention.removeprefix('.')
        self.cache = None
        if read_init:
            self.read()

    def __str__(self):
        return f"File({self.fullname})"

    @property
    def data(self,func = None,):
        '''文件数据'''
        #logger.debug(f'读取{self.abs_path}')
        return self.read(func)

    def read(self,func = None,usecache:bool = True):
        '''读取文件'''
        #logger.debug(f'读取{self.abs_path}')
        return read(self,func,usecache)

    def write(self,*args,func = None,**kwargs):
        '''写入文件'''
        return read(self,*args,func,**kwargs)

class Dire():
    def __init__(self,abs_path):
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f'{abs_path} not exist')
        if not os.path.isdir(abs_path):
            raise IsAFileError(f'{abs_path} is a file')
        self.abs_path = abs_path
        self.files = self.dires = None
        self.name = os.path.basename(abs_path)
        self.files:dict[str,File] = {}
        self.dires:dict[str,'Dire'] = {}
        self.__self_scan()

    def __add_node(self,path) -> None:
        basename = os.path.basename(path)
        if os.path.isfile(path):
            self.files[basename] = File(path)
        elif os.path.isdir(path):
            self.dires[basename] = Dire(path)
        elif os.path.islink(path):
            if ENABLE_SYMLINK_ERROR:
                self.__add_node(os.readlink(path))
            elif ENABLE_SYMLINK_ERROR:
                raise SymbolLinkError(f'{path} is a symbol link')
        else:
            raise NotImplementedError(f'Cannot judge type of {path}, it is not a file, directory, or a symbol link.')

    def __should_be_ingore(self,name):
        basename = os.path.basename(name)
        for prefix in INGORE_PREFIX:
            if basename.startswith(prefix):
                return True
        for suffix in INGORE_SUFFIX:
            if basename.endswith(suffix):
                return True
        return False

    def __self_scan(self):
        self.files = {}
        self.dires = {}
        for rel_path in os.listdir(self.abs_path):
            if ENABLE_INGORE:
                if self.__should_be_ingore(rel_path):
                    continue
            self.__add_node(f'{self.abs_path}{SEP}{rel_path}')

    def scan_subdir(self,patten:Union[str|re.Pattern] = ALL):
        '''和 `scan` 效果相似，函数会返回该文件夹所有下边的一层文件夹的指定文件列表'''
        return self.scan(patten=patten,recur=True,min_recur_deepth=1,max_recur_deepth=1)

    def scan(self,patten:Union[str|re.Pattern] = ALL,
         recur:bool=False,dire_patten:Union[str|re.Pattern] = ALL,
         min_recur_deepth:int = 0,max_recur_deepth:Union[int|None] = sys.maxsize,
         include_dires:bool = False,include_files:bool = True
         ) -> List[File]:
        '''遍历文件夹下所有文件夹所有文件, 读取其中符合正则表达式的文件, 最后以列表形式输出
        ## 参数
        ### 常规
            * `[patten]` 文件需要满足的正则，默认 `".*"`
            * `[include_dires]` 指示递归遍历时输出是否包含子文件夹，默认为 `false`
            * `[include_files]` 指示递归遍历时输出是否包含子文件，默认为 `true`
        ### 递归模式
            * `[recur]` 指示是否递归子文件夹，默认 `False`
            * `[dire_patten]` 文件夹需要满足的正则，默认 `".*"`
            * `[min_recur_deepth]` 遍历的最小深度，默认为 `0`
            * `[max_recur_deepth]` 遍历的最大深度，默认为 `sys.maxsize`
        '''
        if not (self.files or self.dires):
            self.__self_scan()
        if not patten:
            patten = ALL
        output = []
        if min_recur_deepth <= 0 :
            if include_files:
                for filename in self.files:
                    if re.match(patten,filename):
                        output.append(self.files[filename])
            if include_dires:
                for direname in self.dires:
                    if re.match(patten,direname):
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
