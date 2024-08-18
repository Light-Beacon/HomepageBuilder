from typing import Dict, List
from .logger import Logger
from .i18n import locale

events:Dict[str,List[callable]] = {}
logger = Logger('Event')

def trigger_invoke(event_name:str):
    '''在函数开始时触发事件'''
    def wrapper(func):
        def inner_wrapper(*args,**kwagrs):
            trigger_event(event_name,*args,**kwagrs)
            return func(*args,**kwagrs)
        return inner_wrapper
    return wrapper

def trigger_return(event_name:str,return_name='result'):
    '''在函数返回时触发事件'''
    def wrapper(func):
        def inner_wrapper(*args,**kwagrs):
            result = func(*args,**kwagrs)
            kwagrs[return_name] = result
            trigger_event(event_name,*args,**kwagrs)
            return result
        return inner_wrapper
    return wrapper

def trigger_failed(event_name:str, re_arise = True):
    '''在函数出错时触发事件'''
    def wrapper(func):
        def inner_wrapper(*args,**kwagrs):
            try:
                return func(*args,**kwagrs)
            except Exception as ex:
                kwagrs['exception'] = ex
                trigger_event(event_name, *args,**kwagrs)
                if re_arise:
                    raise ex
        return inner_wrapper
    return wrapper

def triggers(event_name:str):
    '''在函数开始时、返回、和出错时触发事件'''
    def wrapper(func):
        @trigger_invoke(event_name + '.start')
        @trigger_return(event_name + '.return')
        @trigger_failed(event_name + '.failed')
        def inner_wrapper(*args,**kwagrs):
            return func(*args,**kwagrs)
        return inner_wrapper
    return wrapper

def listen_event(event_name:str):
    '''监听事件'''
    def wrapper(func):
        if event_name not in events:
            events[event_name] = []
        events[event_name].append(func)
    return wrapper

def trigger_event(event_name:str,*args,**kwargs):
    logger.event(locale('event.triggered',event_name=event_name))
    actions_list = events.get(event_name)
    if not actions_list:
        return
    for action in actions_list:
        action(*args,**kwargs)