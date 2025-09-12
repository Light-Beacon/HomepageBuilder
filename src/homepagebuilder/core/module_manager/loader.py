import os
from pathlib import Path
import importlib
import sys
import re
from types import ModuleType
from typing import List, Union
import asyncio
from concurrent.futures import ThreadPoolExecutor
from ..logger import Logger
from ..i18n import locale as t
from ..io import file_reader, Dire
from ..types import Context
from .manager import modules

PY_PATTERN = re.compile(r'.*\.py$')

logger = Logger('ModuleManager')
class RequireDependency(Exception):
    '''需求依赖例外'''
    def __init__(self, require_module_name:str):
        self.require = require_module_name

class DependencyManager():
    '''模块依赖管理器'''
    def __init__(self):
        self.load_checks: dict[str, list[Path]] = {}
        self.wait_checks: dict[Path, int] = {}

    def require(self,rde:RequireDependency,path:Path) -> None:
        '''需求某项依赖'''
        require_dependency = rde.require
        if require_dependency not in self.load_checks:
            self.load_checks[require_dependency] = []
        self.load_checks[require_dependency].append(path)
        if path not in self.wait_checks:
            self.wait_checks[path] = 1
        else:
            self.wait_checks[path] += 1

    def satisfied(self,module_name) -> List[Path]:
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
class UnLoadedModule():
    '''未加载的模块占位符类'''
    def __init__(self,path):
        self.path = path

dependency_manager = DependencyManager()

def get_check_list():
    return dependency_manager.get_check_list()

def load_module(module_path:Path, queue_load:bool=False):
    '''导入模块'''
    path_to = str(module_path.parent)
    file_name = module_path.name
    name,_ = os.path.splitext(file_name)
    if name in modules :
        # Module already exist
        logger.debug(t('module.reload',name=name))
        module = importlib.reload(modules[name])
    else:
        if not queue_load:
            logger.debug(t('module.load',name=name))
        # Add module
        sys.path.append(path_to)
        try:
            module = importlib.import_module(name)
        except RequireDependency as rd:
            # 如果请求加载某些模块
            dependency_manager.require(rd, module_path)
            return UnLoadedModule(module_path)
        if hasattr(module,'init'):
            getattr(module,'init')(Context.get_current_context())
        logger.debug(t('module.load.success',name=name))
        modules[name] = module
        for module_name in dependency_manager.satisfied(name):
            # 依赖已经成功加载需要重新加载的模块
            load_module(module_name, True)
    return module


async def load_module_async(module_path: Path, queue_load: bool = False):
    '''异步导入模块'''
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        return await loop.run_in_executor(executor, load_module, module_path, queue_load)

async def load_modules_batch_async(module_paths: List[Path]):
    '''批量异步加载模块'''
    with ThreadPoolExecutor(max_workers=10) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(executor, load_module, path)
            for path in module_paths
        ]
        return await asyncio.gather(*tasks)

def require(module_name):
    '''直到模块被成功加载后再加载此模块，并返回需要的模块'''
    required_module = modules.get(module_name)
    if required_module:
        return required_module
    else:
        raise RequireDependency(module_name)

@file_reader('py','python')
def read_python(filepath:Path) -> Union[UnLoadedModule, ModuleType]:
    ''' 读取 Python 文件 '''
    if not filepath.exists():
        raise FileNotFoundError(f'{filepath} not exist!')
    return load_module(filepath)

def load_module_dire(dire, *args, **kwargs):
    ''' 载入文件夹下的所有 python 模块 '''
    modulelist = []
    if isinstance(dire, (str, Path)):
        try:
            dire = Dire(dire)
        except FileNotFoundError:
            return
    if not isinstance(dire, Dire):
        raise TypeError()
    # 收集所有需要加载的文件路径
    file_paths = [file.abs_path for file in dire.scan(PY_PATTERN, recur=True)]
    # 异步批量加载模块
    if file_paths:
        modulelist = asyncio.run(load_modules_batch_async(file_paths))
        # 过滤掉 UnLoadedModule 实例
        modulelist = [mod for mod in modulelist if not isinstance(mod, UnLoadedModule)]
