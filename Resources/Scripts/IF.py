def script(eq_expression:str,true_return,false_return='',**kwargs):
    card = kwargs['card']
    eq_expression.replace(' ','')
    return true_return if iseq(eq_expression,card) else false_return 

def iseq(eq_expression,card) -> bool:
    if '=' in eq_expression:
        eqexp_left, eqexp_right = eq_expression.split('=',1)
        eqexp_left = format_eq(eqexp_left,card)
        eqexp_right = format_eq(eqexp_right,card)
        if eqexp_left == eqexp_right:
            return True
    else:
        if eq_expression.startswith('!'):
            if format_eq(eq_expression[1:],card) in ['false','null','none', None]:
                return True
        else:
            if format_eq(eq_expression,card) not in ['false','null','none', None]:
                return True
    return False
        
def format_eq(expression:str,card):
    if(expression.startswith('$')):
        return card.get(expression[1:])
    else:
        return expression