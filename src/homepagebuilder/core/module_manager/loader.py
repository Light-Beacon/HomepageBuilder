import os
import importlib
import sys
import re
from typing import List
from ..logger import Logger
from ..i18n import locale as t
from ..io import file_reader, Dire
from .manager import modules

PY_PATTERN = re.compile(r'.*\.py$')

logger = Logger('ModuleManager')
class RequireDependency(Exception):
    '''需求依赖例外'''
    def __init__(self,require):
        self.require = require

class DependencyManager():
    '''模块依赖管理器'''
    def __init__(self):
        self.load_checks = {}
        self.wait_checks = {}

    def require(self,rde:RequireDependency,path:str) -> None:
        '''需求某项依赖'''
        require = rde.require
        if require not in self.load_checks:
            self.load_checks[require] = []
        self.load_checks[require].append(path)
        if path not in self.wait_checks:
            self.wait_checks[path] = 1
        else:
            self.wait_checks[path] += 1

    def satisfied(self,module_name) -> List[str]:
        '''标记该项依赖满足，返回该项依赖满足后应当重载的模块列表'''
        if module_name not in self.load_checks:
            return []
        needs_load_modules = []
        for module_path in self.load_checks[module_name]:
            self.wait_checks[module_path] -= 1
            if self.wait_checks[module_path] <= 0:
                needs_load_modules.append(module_path)
                self.wait_checks.pop(module_path)
        self.load_checks.pop(module_name)
        return needs_load_modules

    def get_check_list(self):
        load_checks = list(self.load_checks.keys())
        if len(load_checks) > 0 and load_checks[0]:
            return load_checks
        else:
            return []
class UnLoadedFunction():
    '''未加载的方法占位符类'''
    def __init__(self,path):
        self.path = path

dependency_manager = DependencyManager()

def get_check_list():
    return dependency_manager.get_check_list()

def load_package(dire:Dire):
    logger.debug(dire.abs_path)
    if dire.name == '__pycache__':
        return
    init_file = dire.getfile('__init__.py')
    if not init_file:
        raise ImportError(f'{dire.abs_path} is not a python package')
    parent_path = dire.parent.abs_path
    if parent_path not in sys.path:
        sys.path.append(parent_path)
    package_name = dire.name
    spec = importlib.util.spec_from_file_location(package_name, init_file.abs_path)
    package = importlib.util.module_from_spec(spec)
    sys.modules[package_name] = package
    modules[dire.abs_path] = package
    spec.loader.exec_module(package)
    return package

def load_module(module_path:str, package:str = None, queue_load:bool=False):
    '''导入模块'''
    path_to = os.path.dirname(module_path)
    file_name = os.path.basename(module_path)
    name,_ = os.path.splitext(file_name)
    if module_path in modules :
        # Module already exist
        logger.debug(t('module.reload',name = name))
        module = importlib.reload(modules[module_path])
    else:
        if not queue_load:
            if package:
                logger.debug(t('module.load.frompackage', name = name,
                            package = package.split(os.sep)[-1]))
            else:
                logger.debug(t('module.load.start', name = name))
        # Add module
        sys.path.append(path_to)
        try:
            module = importlib.import_module(name, package = package)
        except RequireDependency as rd:
            # 如果请求加载某些模块
            dependency_manager.require(rd,module_path)
            return UnLoadedFunction(module_path)
        except ImportError as ex:
            logger.error(t('module.load.failed',module = module_path, ex = ex))
            return UnLoadedFunction(module_path)
        logger.debug(t('module.load.success',name=name))
        modules[module_path] = module
        for module in dependency_manager.satisfied(name):
            # 依赖已经成功加载需要重新加载的模块
            load_module(module, package, queue_load=True)
    return module

def init_modules(modulelist,*args,**kwargs):
    '''调用所有模块的`init`方法'''
    for module in modulelist:
        if hasattr(module,'init'):
            getattr(module,'init')(*args,**kwargs)

def require(module_name):
    '''直到模块被成功加载后再加载此模块，并返回需要的模块'''
    required_module = modules.get(module_name)
    if required_module:
        return required_module
    else:
        raise RequireDependency(module_name)

@file_reader(['py','python'])
def read_python(filepath:str, package = None, *_args, **_kwargs) -> callable:
    ''' 读取 Python 文件 '''
    if not os.path.exists(filepath):
        raise FileNotFoundError(f'{filepath} not exist!')
    return load_module(filepath, package)

def load_module_dire(dire, *args, **kwargs):
    ''' 载入文件夹下的所有 python 模块 '''
    modulelist = []
    if isinstance(dire,str):
        try:
            dire = Dire(dire)
        except FileNotFoundError:
            return
    if not isinstance(dire,Dire):
        raise TypeError()
    for file in dire.scan(PY_PATTERN):
        modulelist.append(file.read())
    for dire in dire.scan(PY_PATTERN, include_dires=True, include_files=False):
        load_package(dire)
    init_modules(modulelist,*args,**kwargs)
