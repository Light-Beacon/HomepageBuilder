import re
from typing import Any, Callable, Dict
from .Debug import LogWarning

def format_code(code:str,card,resources,children_code):
    '''格式化代码'''
    pattern = r'\$\{([^}]+)\}'
    matches = re.findall(pattern, code)
    for match in matches:
        qurey_tuple = match.split('|')
        attr_name = qurey_tuple[0]
        if attr_name.startswith('$'):
            replacement = runScript(qurey_tuple[0][1:],resources,card,qurey_tuple,children_code)
        elif attr_name in card:
            replacement = str(card[attr_name])
        else:
            continue
        code = code.replace(f'${{{match}}}',replacement,1)
    return code

script: Callable[[Dict,Any], str]
def runScript(script_name:str,resources,card,args,children_code):
    '''获取脚本输出结果'''
    scripts = resources.scripts
    if(script_name == 'ChildrenPresenter'):
        return children_code
    script_code = scripts.get(script_name)
    if script_code is None:
        LogWarning(f'[Formatter] 尝试调用不存在的脚本: {script_name}')
        return ''
    exec(script_code,globals())
    result = str(script(card,args,resources))
    result = format_code(result,card,resources,children_code)
    return result