def LogInfo(infomation:str):
    print(f'{blue}[INFO]{clear}{infomation}')

def LogWarning(infomation:str):
    print(f'{yellow}[WARNING]{clear}{infomation}')

def LogDebug(infomation:str):
    print(f'{green}[DEBUG]{clear}{infomation}')
    
def LogError(infomation:str):
    print(f'{red}[ERROR]{infomation}')
    return infomation

def LogFatal(infomation:str):
    print(f'{red}[FATAL]{infomation}')
    return infomation

tabtext = '    '

def FormatXaml(code:str):
    code = code.replace('\n','')
    code = code.replace('\r','')
    new_code = ''
    tab = 0
    mark_slash = False
    mark_end = False
    mark_newline = False
    for i in range(len(code)):
        c = code[i] 
        if c == '>':
            new_code += c
            if not mark_slash and not mark_end:
                tab += 1
            mark_end = False
            mark_newline = True
            continue
        else:
            mark_slash = False
        if c == '/':
            mark_slash = True
            new_code += c
            continue
        if c == '<':
            new_code += '\r\n'
            if code[i+1] == '/':
                tab -= 1
                mark_end = True
            for j in range(tab):
                new_code += tabtext
            new_code += c
            mark_newline = False
            continue
        if c != ' ' and mark_newline:
            new_code += '\r\n'
            for j in range(tab):
                new_code += tabtext
            mark_newline = False
        new_code += c
    return new_code

def print_newlineless(char):
    print(char,end='')

def PrintXaml(code:str):
    code = FormatXaml(code)
    is_in_element = False
    is_in_quote = False
    for c in code:
        if c == ' ':
            if is_in_element and not is_in_quote:
                print_newlineless(magenta)
        if c == '=':
            if is_in_element and not is_in_quote:
                print_newlineless(clear)
        if c == '{':
            if is_in_element and is_in_quote:
                print_newlineless(yellow)
        if c == '}':
            if is_in_element and is_in_quote:
                print_newlineless(c)
                print_newlineless(green)
                continue
        if c == '<':
            print_newlineless(c)
            print_newlineless(red)
            is_in_element = True
            continue
        if c == '"':
            if is_in_element:
                is_in_quote = not is_in_quote
                if is_in_quote:
                    print_newlineless(green)
                else:
                    print_newlineless(c)
                    print_newlineless(magenta)
                    continue
        if c == '>':
            is_in_element = False
            print_newlineless(clear)
        print_newlineless(c)
    print('')

clear = '\033[0m'  
black = '\033[30m'
red = '\033[31m'
green = '\033[32m'
yellow = '\033[33m'
blue = '\033[34m'
magenta = '\033[35m'
cyan = '\033[36m'
white = '\033[37m'