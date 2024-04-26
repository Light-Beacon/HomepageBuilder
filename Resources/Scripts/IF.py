from Core.Code_Formatter import format_code

def script(card,args,res):
    args[1].replace(' ','')
    if '=' in args[1]:
        eqs = args[1].split('=',1)
        if eqs[0] in card and card[eqs[0]] == eqs[1]:
            return args[2]
    else:
        if args[1].startswith('!'):
            if args[1][1:] not in card or args[1][1:].lower() in ['false','null']:
                return args[2]
        if args[1] in card and args[1].lower() not in ['false','null']:
            return args[2]
    if len(args) > 3:
        return args[3]
    return ''