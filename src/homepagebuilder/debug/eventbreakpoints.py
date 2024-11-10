from ..core.utils.event import listen_event
from ..core.config import is_debugging

breakpoints = []

if is_debugging():
    for bp in breakpoints:
        listen_event(bp)(lambda *_args,**_kwargs: breakpoint())

def addbp(eventname):
    breakpoints.append(eventname)