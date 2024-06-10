from Core.code_formatter import format_code

def script(eq_expression:str,true_return,false_return='',**kwargs):
    project = kwargs['proj']
    card = kwargs['card']
    eq_expression.replace(' ','')
    return true_return if iseq(eq_expression,card,project) else false_return 

def iseq(eq_expression,card,project) -> bool:
    if '=' in eq_expression:
        eqexp_left, eqexp_right = eq_expression.split('=',1)
        eqexp_left = format_eq(eqexp_left,card,project)
        eqexp_right = format_eq(eqexp_right,card,project)
        if eqexp_left == eqexp_right:
            return True
    else:
        if eq_expression.startswith('!'):
            if format_eq(eq_expression[1:],card,project).lower() in ['false','null','none']:
                return True
        else:
            if format_eq(eq_expression,card,project).lower() not in ['false','null','none']:
                return True
    return False

def format_eq(expression:str,card,project):
    return format_code(expression,card=card,project=project,children_code='',err_output='false')
