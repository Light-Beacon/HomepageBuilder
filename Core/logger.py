"""
该模块用于输出调试与日志信息
"""
import logging
import os.path
import sys
import time
from Core.config import config

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

TIME_PART_FMT = "[%(asctime)s.%(msecs)03d]"
COLORED_TIME_PART_FMT = CONSOLE_WHITE + TIME_PART_FMT + CONSOLE_CLEAR
LOC_PART_FMT = "[%(name)s|%(filename)s:%(lineno)d]"

class ColorConsoleFormater(logging.Formatter):
    def __init__(self):
        self.super_formatter = logging.Formatter(
            fmt=f'{COLORED_TIME_PART_FMT}{LOC_PART_FMT} %(message)s',
            datefmt='%m/%d|%H:%M:%S')

    def format(self, record):
        level_color_console_str = LEVEL_COLORES.get(record.levelno, CONSOLE_CLEAR)
        level_name = LEVEL_NAMES.get(record.levelno, "UNKNOWN")
        return f"{level_color_console_str}[{level_name}]{CONSOLE_CLEAR}" + self.super_formatter.format(record)

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


CONSOLE_HANDLER = LogConsoleHandler()

current_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
log_pos = os.path.abspath("Log/")
print(log_pos)
if not os.path.exists(log_pos):
    os.makedirs(log_pos)
FILE_HANDLER = logging.FileHandler(f"{log_pos}{os.path.sep}{current_time}.log")
FILE_HANDLER.setFormatter(logging.Formatter(
            fmt=f'[%(levelname)s]{TIME_PART_FMT}{LOC_PART_FMT} %(message)s',
            datefmt='%m/%d|%H:%M:%S'))

is_enable_debug = config('Debug.Enable')
level = 0 if is_enable_debug else config('Debug.Logging.Level')
FILE_HANDLER.setLevel(level)
CONSOLE_HANDLER.setLevel(level)

logging.basicConfig(level=logging.INFO)

class Logger(logging.Logger):
    """日志记录器"""
    def __init__(self, name):
        logging.Logger.__init__(self, name)
        self.addHandler(CONSOLE_HANDLER)
        self.addHandler(FILE_HANDLER)
        self.propagate = False
    
    def event(self, msg, *args, **kwargs):
        self._log(5, msg, args, **kwargs)
