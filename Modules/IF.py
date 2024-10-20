from Builder.Interfaces import script, format_code

@script('IF')
def if_script(eq_expression:str,true_return,false_return='',**kwargs):
    env = kwargs['env']
    card = kwargs['card']
    eq_expression.replace(' ','')
    return true_return if iseq(eq_expression,card,env) else false_return 

def iseq(eq_expression,card,env) -> bool:
    if '=' in eq_expression:
        eqexp_left, eqexp_right = eq_expression.split('=',1)
        eqexp_left = format_eq(eqexp_left,card,env)
        eqexp_right = format_eq(eqexp_right,card,env)
        if eqexp_left == eqexp_right:
            return True
    else:
        if eq_expression.startswith('!'):
            if format_eq(eq_expression[1:],card,env).lower() in ['false','null','none']:
                return True
        else:
            if format_eq(eq_expression,card,env).lower() not in ['false','null','none']:
                return True
    return False

def format_eq(expression:str,card,env):
    return format_code(expression,data=card,env=env,children_code='',err_output='false')
