from typing import Any, Callable, Dict
from .Debug import LogWarning, LogDebug
from .ModuleManager import invokeScript

def format_code(code:str,card:Dict[str,object],
                project,children_code:str='',stack:list = []):
    '''格式化代码'''
    matches = findall_placeholders(code)
    for match in matches:
        #LogDebug(str(match))
        qurey_tuple = split_args(match)
        attr_name = qurey_tuple[0]
        if attr_name in stack:
            LogWarning(f'[Formatter] 检测到循环调用: {stack}')
            return code
        for item in qurey_tuple[1:]:
            # 格式化参数
            item = format_code(code=item,card=card,project=project,
                               children_code=children_code,stack=stack)
        if attr_name.startswith('$') or attr_name.startswith('@'):
            replacement = invokeScript(script_name=qurey_tuple[0][1:],
                                    project=project,card=card,args=qurey_tuple[1:],
                                    children_code=children_code)
        elif attr_name in card:
            replacement = str(card[attr_name])
        else:
            if len(qurey_tuple) >= 1:
                replacement = qurey_tuple[-1]
            else:
                LogWarning(f'[Formatter] 访问了不存在的属性，并且没有设定默认值: {attr_name}')
                continue
        stack.append(attr_name)
        try:
            replacement = format_code(replacement,card,project,children_code,stack)
        finally:
            stack.pop()
        code = code.replace(f'${{{match}}}',replacement,1)
    return code

def split_args(string:str):
    args = []
    in_qoute = False
    pare_deepth = 0
    buffer = ''
    for c in string:
        buffer += c
        if in_qoute:
            if c == '"':
                in_qoute = False
        else:
            if c == '{':
                pare_deepth += 1
            if pare_deepth > 0:
                if c == '}':
                    pare_deepth -= 1
            else:
                match c:
                    case '|':
                        args.append(buffer[:-1])
                        buffer = ''
                    case '"':
                        in_qoute = True
    args.append(buffer)
    return args

def findall_placeholders(string:str):
    if string == None:
        return []
    placeholders = []
    pare_deepth = 0
    sp_mode = False
    buffer = ''
    for c in string:
        if pare_deepth > 0:
            if c == '}':
                pare_deepth -= 1
                if pare_deepth == 0:
                    placeholders.append(buffer)
                    buffer = ''
                else:
                    buffer += c
            else:
                buffer += c
        if c == '{' and (sp_mode or pare_deepth > 0):
            pare_deepth += 1
        if c == '$':
            sp_mode = True
        else:
            sp_mode = False
    return placeholders