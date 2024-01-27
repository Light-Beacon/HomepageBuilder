import re
from .scriptRunner import runScript

    
def format_code(code:str,card,scripts):
    '''格式化代码'''
    pattern = r'\{([^}]+)\}'
    matches = re.findall(pattern, code)
    for match in matches:
        qurey_tuple = match.split('|')
        attr_name = qurey_tuple[0]
        if attr_name.startswith('$'):
            replacement = runScript(scripts[qurey_tuple[0][1:]],card,qurey_tuple)
        elif attr_name in card:
            replacement = card[attr_name]
        else:
            continue
        code = code.replace(f'{{{match}}}',replacement,1)
    return code

if __name__ == '__main__':
    testcode = '{test1}-{$f1|666}-{$f1|233}'
    card = {'test1':'sss','mem':'0'}
    def func1(c,args):
        c['mem'] = str(int(c['mem'])+1)
        return c['mem'] + args[1]
    s = {'f1':func1}
    print(format_code(testcode,card,s))