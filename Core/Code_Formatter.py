import re
from typing import Any, Callable, Dict

def format_code(code:str,card,scripts,children_code):
    '''格式化代码'''
    pattern = r'\{([^}]+)\}'
    matches = re.findall(pattern, code)
    for match in matches:
        qurey_tuple = match.split('|')
        attr_name = qurey_tuple[0]
        if attr_name.startswith('$'):
            replacement = runScript(qurey_tuple[0][1:],scripts,card,qurey_tuple,children_code)
        elif attr_name in card:
            replacement = card[attr_name]
        else:
            continue
        code = code.replace(f'{{{match}}}',replacement,1)
    return code

script: Callable[[Dict,Any], str]
def runScript(script_name:str,scripts:Dict[str,str],card,args,children_code):
    if(script_name == 'ChildrenPresenter'):
        return children_code
    script_code = scripts.get(script_name)
    if script_code is None:
        # TODO: Script Not Found
        pass
    exec(script_code,globals())
    result = str(script(card,args))
    result = format_code(result,card,scripts,children_code)
    return result

if __name__ == '__main__':
    testcode = '{test1}-{$f1|666}-{$f1|233}'
    card = {'test1':'sss','mem':'0'}
    def func1(c,args):
        c['mem'] = str(int(c['mem'])+1)
        return c['mem'] + args[1]
    s = {'f1':func1}
    print(format_code(testcode,card,s))