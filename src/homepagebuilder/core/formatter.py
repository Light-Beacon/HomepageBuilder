"""
该模块用于格式化代码
"""
from typing import Dict, TYPE_CHECKING
from .logger import Logger
from .module_manager import invoke_script

if TYPE_CHECKING:
    from .types import Context


logger = Logger('Formatter')
def format_code(code: str,
                data: Dict[str,object],
                context: 'Context',
                children_code: str = '',
                stack:list = None,
                err_output = None):
    '''格式化代码'''
    if not isinstance(code,str):
        return code
    if not stack:
        stack = []
    project = context.project
    code = str(code)
    matches = findall_placeholders(code)
    for match in matches:
        #LogDebug(str(match))
        qurey_tuple = split_args(str(match))
        attr_name = qurey_tuple[0]
        if code in stack:
            logger.warning(f'检测到循环调用: {stack}')
            return code
        #for item in qurey_tuple[1:]:
            # 格式化参数
        #    item = format_code(code=item,card=card,project=project,
        #                       children_code=children_code,stack=stack)
        if attr_name.startswith('$') or attr_name.startswith('@'):
            script_name=qurey_tuple[0][1:]
            replacement = invoke_script(script_name=script_name,
                                    project=project,context=context,card=data,args=qurey_tuple[1:],
                                    children_code=children_code)
        else:
            try:
                replacement = get_card_prop(data,attr_name)
            except Exception:
                if err_output:
                    return err_output
                if len(qurey_tuple) >= 1:
                    replacement = qurey_tuple[-1]
                else:
                    logger.warning(f'访问了不存在的属性，并且没有设定默认值: {attr_name}')
                    continue
        stack.append(code)
        try:
            replacement = format_code(replacement,data,context,children_code,stack)
        finally:
            stack.pop()
        code = code.replace(f'${{{match}}}',str(replacement),1)
    return code

def get_card_prop(card,attr_name):
    return dfs_get_prop(card,attr_name)

def dfs_get_prop(current_tree,prop_path:str):
    if '.' not in prop_path:
        return current_tree[prop_path]
    this_name,next_path = prop_path.split('.',maxsplit=2)
    if next_tree := current_tree.get(this_name):
        return dfs_get_prop(next_tree,next_path)
    else:
        raise PropNotFoundError(prop_path)

class PropNotFoundError(Exception):
    def __init__(self, key, *args,):
        super().__init__(*args)
        self.key = key

class PropNotFormatedError(Exception):
    def __init__(self, key, *args,):
        super().__init__(*args)
        self.key = key

def split_args(string:str):
    '''分离参数'''
    args = []
    string = str(string)
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
    '''寻找全部占位符'''
    if not string:
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
