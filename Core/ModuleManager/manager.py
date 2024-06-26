def invoke_module(modulename:str,funcname:str) -> callable:
    '''调用某模块的方法'''
    if module := modules.get(modulename):
        return getattr(module,funcname)
    else:
        raise ModuleNotFoundError

modules = {}