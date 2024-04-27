import importlib
import os
import sys
from typing import Dict, Callable, Any
from .Debug import LogInfo, LogWarning, LogDebug

class RequireDependency(Exception):
    def __init__(self,*require):
        self.requires = []
        for req in require:
            self.requires.append(req)

class DependencyManager():
    def __init__(self):
        self.load_checks = {}
        self.wait_checks = {}
    
    def require(self,rde:RequireDependency,path:str) -> None:
        for require in rde.requires:
            if require not in self.load_checks:
                self.load_checks[require] = []
            self.load_checks[require].append(path)
        self.wait_checks[path] = len(rde.requires)

    def satisfied(self,module_name):
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

class UnLoadedFunction():
    # 占位符类
    def __init__(self,path):
        self.path = path

dependencyManager = DependencyManager()
scripts_modules = {}
temp_storied_scripts = {}

def RegScript(script_path,queue_load:bool=False):
    path_to = os.path.dirname(script_path)
    file_name = os.path.basename(script_path)
    name,exten = os.path.splitext(file_name)
    if name in scripts_modules :
        # Module already exist
        LogInfo(f'[Scripts] Reloading script: {name}')
        module = importlib.reload(scripts_modules[name])
    else:
        if not queue_load:
            LogInfo(f'[Scripts] Loading script: {name}')
        # Add module
        sys.path.append(path_to)
        try:
            module = importlib.import_module(f'{name}')
        except RequireDependency as rd:
            # 如果请求加载某些模块
            dependencyManager.require(rd,script_path)
            # LogDebug(f'[Scripts] Script {name} requires {str.join(',',rd.requires)}, will delay to be loaded until these dependencies satisfied.')
            return UnLoadedFunction(script_path)
        LogInfo(f'[Scripts] Successfully loaded script: {name}')
        scripts_modules[name] = module
        for module in dependencyManager.satisfied(name):
            # 依赖已经成功加载需要重新加载的模块
            newfunc,newname = RegScript(module,True)
            # LogDebug(f'[Scripts] Script {newname} dependencies satisfied and loaded')
            temp_storied_scripts[newname] = newfunc
    if hasattr(module,'script'):
        func = getattr(module,'script')
        if not callable(func):
            raise Exception(f'{script_path} script not callable')
    else:
        return None
    if queue_load:
        return func,name
    return func

def storgeTempScripts(scripts):
    '''加载已经加载完但是还没有写入资源字典的脚本'''
    scripts.update(temp_storied_scripts)
    temp_storied_scripts.clear()

script: Callable[[Dict,Any], str]
def invokeScript(script_name:str,project,card:Dict[str,object],
              args:list,children_code:str):
    '''获取脚本输出结果'''
    resources = project.resources
    scripts = resources.scripts
    if script_name == 'ChildrenPresenter':
        return children_code
    script_code = scripts.get(script_name)
    if script_code is None:
        LogWarning(f'[Formatter] 尝试调用不存在的脚本: {script_name}')
        return ''
    result = scripts[script_name](*args,card=card,res=resources,proj=project)
    return result

def invokeModule(modulename:str,funcname:str):
    if module := scripts_modules.get(modulename):
        return getattr(module,funcname)
    else:
        raise ModuleNotFoundError
    
def untilLoaded(*args):
    requireed_modules = []
    for module in args:
        if module not in scripts_modules:
            requireed_modules.append(module)
    if len(requireed_modules) > 0:
        raise RequireDependency(*requireed_modules)