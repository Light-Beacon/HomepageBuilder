'''
该模块用于输出调试与日志信息
'''
def log_info(infomation:str):
    '''输出信息'''
    print(f'{CONSOLE_BLUE}[INFO]{CONSOLE_CLEAR}{infomation}')

def log_warning(infomation:str):
    '''输出警告'''
    print(f'{CONSOLE_YELLOW}[WARNING]{CONSOLE_CLEAR}{infomation}')

def log_debug(infomation:str):
    '''输出调试信息'''
    print(f'{CONSOLE_GREEN}[DEBUG]{CONSOLE_CLEAR}{infomation}')

def log_error(infomation:str):
    '''输出错误信息'''
    print(f'{CONSOLE_RED}[ERROR]{infomation}')
    return infomation

def log_fatal(infomation:str):
    '''输出致命错误信息'''
    print(f'{CONSOLE_RED}[FATAL]{infomation}')
    return infomation

TAB_TEXT = '    '
CONSOLE_CLEAR = '\033[0m'
CONSOLE_BLACK = '\033[30m'
CONSOLE_RED = '\033[31m'
CONSOLE_GREEN = '\033[32m'
CONSOLE_YELLOW = '\033[33m'
CONSOLE_BLUE = '\033[34m'
CONSOLE_MAGENTA = '\033[35m'
CONSOLE_CYAN = '\033[36m'
CONSOLE_WHITE = '\033[37m'
