import functools
from enum import Enum
from typing import Dict, List
from ..logger import Logger
from ..i18n import locale
import threading

EVENTS: Dict[str,List[callable]] = {}
EVENT_LOCK = threading.Lock()
logger = Logger('Event')

class CallingStatus(Enum):
    error = -1
    starting = 0
    running = 1
    blocked = 2
    returning = 3
    returned = 4

class FunctionContext:
    args: List[object]
    kwargs: Dict[str, object]

    @property
    def status(self) -> CallingStatus:
        """Status of the current function"""
        raise NotImplementedError

    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs

class FunctionStaring(FunctionContext):
    @property
    def status(self) -> CallingStatus:
        return CallingStatus.starting

class FunctionReturned(FunctionContext):
    result: object

    @property
    def status(self) -> CallingStatus:
        return CallingStatus.returned

    def __init__(self, args, kwargs, result):
        self.result = result
        super().__init__(args, kwargs)

class FunctionError(FunctionContext):
    exception: Exception

    @property
    def status(self) -> CallingStatus:
        return CallingStatus.error

    def __init__(self, args, kwargs, exception):
        self.exception = exception
        super().__init__(args, kwargs)

class Event:
    """事件"""
    name: str

    def __init__(self, name):
        self.name = name

    def trigger(self):
        """触发事件"""
        with EVENT_LOCK:
            if self.name in EVENTS:
                for callback in EVENTS[self.name]:
                    try:
                        callback(self)
                    except Exception as e:
                        logger.error(locale('event.error',
                                            eventname=self.name, ex=e))
                        raise e

class FunctionEvent(Event):
    """函数事件"""
    caller: FunctionContext

    def __init__(self, name, caller):
        super().__init__(name)
        self.caller = caller

def set_triggers(event_name:str):
    '''在函数开始时、返回、和出错时触发事件'''
    def wrapper(func):
        @functools.wraps(func)
        def function_triggers(*args, **kwargs):
            try:
                FunctionEvent(event_name + '.start',
                    FunctionStaring(args,kwargs)).trigger()
                result = func(*args, **kwargs)
                FunctionEvent(event_name + '.return',
                    FunctionReturned(args,kwargs,result)).trigger()
                return result
            except ResultOverride as ro:
                return ro.result
            except Exception as ex:
                try:
                    FunctionEvent(event_name + '.failed',
                        FunctionError(args,kwargs,ex)).trigger()
                except ResultOverride as e:
                    return e.result
                except Exception as e:
                    raise e
        return function_triggers
    return wrapper

def listen_event(event_name:str):
    '''监听事件'''
    def wrapper(func):
        logger.debug(locale('event.subscribe',
                            func=f'{func.__module__.replace("homepagebuilder.","Builder.")}:{func.__name__}',
                            name=event_name))
        if event_name not in EVENTS:
            EVENTS[event_name] = []
        EVENTS[event_name].append(func)
    return wrapper

class ResultOverride(Exception):
    """在事件中抛出该异常以停止原函数以及尚未执行的触发器运行并输出结果"""
    def __init__(self, result):
        self.result = result
