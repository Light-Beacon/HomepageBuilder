"""
该模块用于输出调试与日志信息
"""
import logging
import os.path
import sys
import time
from .config import config, is_debugging, subscribe_debug_changing

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

LEVEL_COLORES = {
    5: CONSOLE_CYAN,
    10: CONSOLE_GREEN,
    20: CONSOLE_BLUE,
    30: CONSOLE_YELLOW,
    40: CONSOLE_RED,
    50: CONSOLE_MAGENTA}

LEVEL_NAMES = {
    5: "EVENT",
    10: "DEBUG",
    20: "INFO",
    30: "WARNING",
    40: "ERROR",
    50: "CRITICAL"}


def supports_color():
    # 检查是否为 Windows 系统
    if os.name == 'nt':
        return 'ANSICON' in os.environ or 'WT_SESSION' in os.environ
    # 对于其他系统，检查是否连接到终端
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

TIME_PART_FMT = "[%(asctime)s.%(msecs)03d]"
COLORED_TIME_PART_FMT = CONSOLE_WHITE + TIME_PART_FMT + CONSOLE_CLEAR
LOC_PART_FMT = "[%(name)s|%(filename)s:%(lineno)d]"
IS_CONSOLE_SUPPORTS_COLOR = supports_color()


class ColorConsoleFormater(logging.Formatter):
    def __init__(self):
        if IS_CONSOLE_SUPPORTS_COLOR:
            self.super_formatter = logging.Formatter(
                fmt=f'{COLORED_TIME_PART_FMT}{LOC_PART_FMT} %(message)s',
                datefmt='%m/%d|%H:%M:%S')
        else:
            self.super_formatter = logging.Formatter(
                fmt=f'{TIME_PART_FMT}{LOC_PART_FMT} %(message)s',
                datefmt='%m/%d|%H:%M:%S')

    def format(self, record):
        level_color_console_str = ''
        level_name = LEVEL_NAMES.get(record.levelno, "UNKNOWN")
        if IS_CONSOLE_SUPPORTS_COLOR:
            level_color_console_str = LEVEL_COLORES.get(record.levelno, CONSOLE_CLEAR)
            return f"{level_color_console_str}[{level_name}]{CONSOLE_CLEAR}" + self.super_formatter.format(record)
        else:
            return f"[{level_name}]{self.super_formatter.format(record)}"
        
CONSOLE_FORMATTER = ColorConsoleFormater()

class LogConsoleHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self.level = 0
        self.errStreamHandler = logging.StreamHandler(sys.stderr)
        self.errStreamHandler.setFormatter(CONSOLE_FORMATTER)
        self.outStreamHandler = logging.StreamHandler(sys.stdout)
        self.outStreamHandler.setFormatter(CONSOLE_FORMATTER)

    def emit(self, record):
        if record.levelno >= logging.ERROR:
            self.errStreamHandler.emit(record)
        else:
            self.outStreamHandler.emit(record)


def init_file_handler():
    current_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
    log_pos = os.path.abspath("Log/")
    print(log_pos)
    if not os.path.exists(log_pos):
        os.makedirs(log_pos)
    handler = logging.FileHandler(f"{log_pos}{os.path.sep}{current_time}.log")
    handler.setFormatter(logging.Formatter(
                fmt=f'[%(levelname)s]{TIME_PART_FMT}{LOC_PART_FMT} %(message)s',
                datefmt='%m/%d|%H:%M:%S'))
    return handler

CONSOLE_HANDLER = None
FILE_HANDLER = None
if config('Debug.Logging.ConsoleOutput.Enable', True):
    CONSOLE_HANDLER = LogConsoleHandler()

if config('Debug.Logging.FileOutput.Enable', False):
    FILE_HANDLER = init_file_handler()

IS_DEBUG_ENABLE = None
LOGGING_LEVEL = None
def set_logging_level():
    global IS_DEBUG_ENABLE, LOGGING_LEVEL
    IS_DEBUG_ENABLE = is_debugging()
    LOGGING_LEVEL = config('Debug.Logging.Level') if IS_DEBUG_ENABLE else config('Logging.Level')
    if CONSOLE_HANDLER:
        CONSOLE_HANDLER.setLevel(LOGGING_LEVEL)
    if FILE_HANDLER:
         CONSOLE_HANDLER.setLevel(LOGGING_LEVEL)

subscribe_debug_changing(set_logging_level)
set_logging_level()

logging.basicConfig(level=logging.INFO)

class Logger(logging.Logger):
    """日志记录器"""
    def __init__(self, name):
        logging.Logger.__init__(self, name)
        if CONSOLE_HANDLER:
            self.addHandler(CONSOLE_HANDLER)
        if FILE_HANDLER:
            self.addHandler(FILE_HANDLER)
        self.propagate = False
    
    def event(self, msg, *args, **kwargs):
        self._log(5, msg, args, **kwargs)
