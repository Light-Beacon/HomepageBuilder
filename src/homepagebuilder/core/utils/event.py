import functools
from typing import Dict, List
from ..logger import Logger
from ..i18n import locale

events:Dict[str,List[callable]] = {}
logger = Logger('Event')

def set_triggers(event_name:str):
    '''在函数开始时、返回、和出错时触发事件'''
    def wrapper(func):
        @functools.wraps(func)
        def function_triggers(*args,**kwagrs):
            try:
                trigger_event(event_name + '.start',*args,**kwagrs)
                result = func(*args,**kwagrs)
                trigger_event(event_name + '.return',*args ,result = result, **kwagrs)
                return result
            except ResultOverride as ro:
                return ro.result
            except Exception as ex:
                try:
                    trigger_event(event_name + '.failed', *args,exception = ex, **kwagrs)
                except ResultOverride as e:
                    return e.result
                finally:
                    raise ex
        return function_triggers
    return wrapper

def listen_event(event_name:str):
    '''监听事件'''
    def wrapper(func):
        logger.debug(locale('event.subscribe',
                            func=f'{func.__module__.replace("homepagebuilder.","Builder.")}:{func.__name__}',
                            name=event_name))
        if event_name not in events:
            events[event_name] = []
        events[event_name].append(func)
    return wrapper

def trigger_event(event_name:str,*args,**kwargs):
    #logger.event(locale('event.triggered',event_name=event_name))
    actions_list = events.get(event_name)
    if not actions_list:
        return
    for action in actions_list:
        try:
            action(*args,**kwargs)
        except ResultOverride as ro:
            raise ro
        except Exception as ex:
            logger.error(locale('event.error',event_name=event_name, ex=ex))
            raise ex

class ResultOverride(Exception):
    """在事件中抛出该异常以停止原函数以及尚未执行的触发器运行并输出结果"""
    def __init__(self, result):
        self.result = result