from homepagebuilder.interfaces import script, format_code

@script('IF')
def if_script(eq_expression:str,true_return,false_return='',**kwargs):
    context = kwargs['context']
    card = kwargs['card']
    eq_expression.replace(' ','')
    return true_return if iseq(eq_expression,card,context) else false_return 

def iseq(eq_expression,card,context) -> bool:
    if '=' in eq_expression:
        eqexp_left, eqexp_right = eq_expression.split('=',1)
        eqexp_left = format_eq(eqexp_left,card,context)
        eqexp_right = format_eq(eqexp_right,card,context)
        if eqexp_left == eqexp_right:
            return True
    else:
        if eq_expression.startswith('!'):
            if format_eq(eq_expression[1:],card,context).lower() in ['false','null','none']:
                return True
        else:
            if format_eq(eq_expression,card,context).lower() not in ['false','null','none']:
                return True
    return False

def format_eq(expression:str,card,context):
    return format_code(expression,data=card,context=context,children_code='',err_output='false')
