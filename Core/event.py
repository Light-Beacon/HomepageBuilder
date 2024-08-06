from typing import Dict, List

events:Dict[str,List[callable]] = {}

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
                func(*args,**kwagrs)
            except Exception as ex:
                kwagrs['exception'] = ex
                trigger_event(event_name, *args,**kwagrs)
                if re_arise:
                    raise ex
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
    actions_list = events.get(event_name)
    if not actions_list:
        return
    for action in actions_list:
        action(*args,**kwargs)