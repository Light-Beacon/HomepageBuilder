import time
from ..core.i18n import locale
from ..core.logger import Logger
from ..core.config import config

logger = Logger('Timer')
count = 0
ENABLE_DEBUG = config('Debug.Enable')

def count_time(func:callable):
    def timer_deco(*args,**kwargs):
        global count
        if ENABLE_DEBUG:
            count += 1
            current_count = count
            logger.debug(locale('debug.timer.start',
                                func=func.__name__,count=current_count))
            star_time = time.time()
            output = func(*args,**kwargs)
            end_time = time.time()
            logger.debug(locale('debug.timer.stop',
                                func=func.__name__,count=current_count,
                                time=round(end_time-star_time,4)))
            return output
        else:
            return func(*args,**kwargs)
    return timer_deco
