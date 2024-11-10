
import time
from typing import List

ANLDEBUGGING = False

def repeat(string,times:int):
    s = ''
    for _ in range(0,times):
        s += string
    return s
    

class Phase():
    def __init__(self,name):
        self.name = name
        self.subphases:List['Phase'] = []
        self.__timespan = 0
        self.__start_time = None
        self.__end_time = None
        self.__pasued = False
        self.__ancestor = None
        self.__current_subphase = None

    @property
    def ancesotr(self):
        return self.__ancestor

    @property
    def timespan(self):
        if not self.__start_time:
            raise PhaseNotStartedError(phase = self)
        return self.__timespan

    @property
    def timespan_ms(self):
        return round(self.__timespan*1000)
    
    def start_new_subphase(self,name:str):
        if self.__current_subphase:
            self.__current_subphase.stop()
        subphase = Phase(name)
        subphase.__set_ancestor(self)
        self.__current_subphase = subphase
        self.subphases.append(subphase)
        subphase.start()
        return subphase

    def __set_ancestor(self,ancesotr:'Phase'):
        self.__ancestor = ancesotr

    @property
    def last_subphase(self):
        if len(self.subphases) <= 0:
            return None
        return self.subphases[-1]

    @property
    def start_time(self):
        return self.__start_time
    
    @property
    def end_time(self):
        return self.__end_time

    def start(self):
        self.__checklock()
        if self.__start_time:
            raise PhaseStartedError(phase = self)
        self.__start_time = time.time()
    
    def pasue(self):
        if self.__pasued:
            return
        self.__timespan += self.getspan()
        self.__pasued = True
    
    def resume(self):
        if not self.__pasued:
            return
        self.__start_time = time.time()

    def stop(self):
        if self.__current_subphase:
            self.__current_subphase.stop()
        if self.is_ended():
            return
        self.__end_time = time.time()
        if not self.__pasued:
            self.__timespan += self.getspan(self.__end_time)

    def is_ended(self):
        return bool(self.__end_time)
    
    def __checklock(self):
        if self.__end_time:
            raise PhaseEndedError(phase = self)

    def getspan(self, curtime = None):
        if not curtime:
            curtime = time.time()
        return curtime - self.__start_time

class PhaseNotStartedError(Exception):
    pass

class PhaseStartedError(Exception):
    pass

class PhaseEndedError(Exception):
    pass

class Analyzer():
    def __init__(self, disabled = False) -> None:
        self.__start_time = time.time()
        self.mainphase = Phase('Main')
        self.ancesotrphase = self.mainphase
        self.currentphase = None
        self.mainphase.start()
        self.__disabled = disabled

    def switch_in(self):
        if self.__disabled:
            return
        if not self.currentphase:
            return
        self.ancesotrphase = self.currentphase
        self.currentphase = None

    def switch_out(self):
        if self.__disabled:
            return
        if not self.currentphase.ancesotr:
            raise ReferenceError()
        if not self.currentphase.is_ended():
            self.currentphase.stop()
        self.currentphase = self.ancesotrphase
        self.ancesotrphase = self.currentphase.ancesotr

    def phase(self,name) -> Phase:
        '''阶段'''
        if self.__disabled:
            return None
        self.currentphase = self.ancesotrphase.start_new_subphase(name)
    
    def stop(self):
        if self.mainphase and not self.mainphase.is_ended():
            self.mainphase.stop()

    def pause(self):
        if self.currentphase and not self.currentphase.is_ended():
            self.currentphase.pasue()

    def get_total_time(self):
        return self.mainphase.getspan()

    def __print_phase(self,phase,total_time,deepth:int):
        print(f'{repeat("  ",deepth)}{phase.name}: {phase.timespan_ms}ms {round(phase.timespan * 100 / total_time,2)}%')
        self.__print_subphases(phase,total_time,deepth)
    
    def __print_subphases(self,phase,total_time,deepth:int):
        for subphase in phase.subphases:
            self.__print_phase(subphase,total_time,deepth+1)

    def summarize(self):
        if self.__disabled:
            return
        total_time = self.get_total_time()
        print(repeat('=',26))
        print('TIME COUSUMING SUMMERY:')
        print(repeat('-',26))
        self.__print_subphases(self.mainphase,total_time,-1)
        print(repeat('-',26))
        print(f'TOTAL: {round(self.mainphase.timespan,4)}s {round(self.mainphase.timespan * 100 / total_time,4)}%')
        print(repeat('=',26))
    
    def disable(self):
        self.__disabled = True

global_anlyzer = Analyzer(True)