import importlib
import os
import sys
from .Debug import LogInfo
scripts_modules = {}
def RegScript(script_path):
    path_to = os.path.dirname(script_path)
    file_name = os.path.basename(script_path)
    name,exten = os.path.splitext(file_name)
    if name in scripts_modules :
        # Module already exist
        LogInfo(f'[Scripts] Reloading script: {name}')
        module = importlib.reload(scripts_modules[name])
    else:
        # Add module
        LogInfo(f'[Scripts] Loading script: {name}')
        sys.path.append(path_to)
        module = importlib.import_module(f'{name}')
        scripts_modules[name] = module
    if hasattr(module,'script'):
        func = getattr(module,'script')
        if not callable(func):
            raise Exception(f'{script_path} script not callable')
    else:
        return None
    return func