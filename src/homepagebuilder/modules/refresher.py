from datetime import datetime
from homepagebuilder.interfaces.Events import on
from homepagebuilder.core.config import enable_by_config, config
from homepagebuilder.core.i18n import locale
from homepagebuilder.core.logger import Logger


Logger = Logger('Refresher')
STANDARD_TIME = datetime(2000, 1, 1)

class TimeChecker:
    '''检查时间是否过期'''
    def __init__(self, time_precision: str):
        self.last_check_time = STANDARD_TIME
        self.__checkers = []
        self.__init_checkers(time_precision)

    def __check_same_second(self, now: datetime) -> bool:
        return now.second == self.last_check_time.second

    def __check_same_minute(self, now: datetime) -> bool:   
        return now.minute == self.last_check_time.minute

    def __check_same_hour(self, now: datetime) -> bool:
        return now.hour == self.last_check_time.hour

    def __check_same_day(self, now: datetime) -> bool:
        return now.date() == self.last_check_time.date()

    def __init_checkers(self, time_precision: str):
        if time_precision in ['s']:
            self.__checkers.append(self.__check_same_second)
        if time_precision in ['s','m']:
            self.__checkers.append(self.__check_same_minute)
        if time_precision in ['s','m','h']:
            self.__checkers.append(self.__check_same_hour)
        if time_precision == ['s','m','h','d']:
            self.__checkers.append(self.__check_same_day)

    def check(self) -> bool:
        now = datetime.now()
        for checker in self.__checkers:
            if not checker(now):
                self.last_check_time = datetime.now()
                return True
        return False

CHECKER = None
@on('project.load.return')
def init_checker(proj, *_args, **_kwargs):
    '''初始化时间检查器'''
    global CHECKER
    CHECKER = TimeChecker(config('Refresher.Precision', 's'))
    proj.set_context_data('refresher.checker', CHECKER)

@enable_by_config('Refresher.Enable')
def check_and_clear_cache(server_api):
    '''检查缓存是否过期'''
    if CHECKER.check():
        server_api.clear_cache()
        Logger.debug(locale('refresher.triggered'))

@on('server.get.page.start')
def check_cache_page(server_api, *_args, **_kwargs):
    check_and_clear_cache(server_api)

@on('server.get.json.start')
def check_cache_json(server_api, *_args, **_kwargs):
    check_and_clear_cache(server_api)

@on('server.get.version.start')
def check_cache_version(server_api, *_args, **_kwargs):
    check_and_clear_cache(server_api)
