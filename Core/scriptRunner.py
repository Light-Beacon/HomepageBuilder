from typing import Any, Callable, Dict
script: Callable[[Dict,Any], str]
    
def runScript(script_code:str,card,args):
    exec(script_code,globals())
    return str(script(card,args))