
import time
from typing import List

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
    
    def start_new_subphase(self,name:str):
        if self.__current_subphase:
            self.__current_subphase.stop()
        subphase = Phase(name)
        subphase.__set_ancestor(self)
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
        if self.__start_time:
            raise PhaseStartedError(phase = self)
        self.__start_time = time.time()
    
    def pasue(self):
        if self.__pasued:
            return
        self.__timespan += self.__getspan()
        self.__pasued = True
    
    def resume(self):
        if not self.__pasued:
            return
        self.__start_time = time.time()

    def stop(self):
        if self.__current_subphase:
            self.__current_subphase.stop()
        self.__end_time = time.time()
        self.__timespan += self.getspan(self.__end_time)

    def is_ended(self):
        return bool(self.__end_time)
    
    def __checklock(self):
        if self.__end_time:
            raise PhaseEndedError(phase = self)

    def getspan(self, curtime = time.time()):
        return curtime - self.__start_time

class PhaseNotStartedError(Exception):
    pass

class PhaseStartedError(Exception):
    pass

class PhaseEndedError(Exception):
    pass


class Analyzer():
    def __init__(self) -> None:
        self.__start_time = time.time()
        self.mainphase = Phase('Main')
        self.ancesotrphase = self.mainphase
        self.currentphase = None
        self.mainphase.start()

    @property
    def phase(self):
        return self.currentphase

    def switch_in(self):
        if not self.currentphase:
            return
        self.ancesotrphase = self.currentphase
        self.currentphase = None

    def switch_out(self):
        if not self.currentphase.ancesotr:
            raise 
        if not self.currentphase.is_ended():
            self.currentphase.stop()
        self.currentphase = self.ancesotrphase
        self.ancesotrphase = self.currentphase.ancesotr

    def phase(self,name) -> Phase:
        '''阶段'''
        self.currentphase = self.ancesotrphase.start_new_subphase('name')
    
    def stop(self):
        if self.mainphase and not self.mainphase.is_ended():
            self.mainphase.stop()

    def get_total_time(self):
        return self.mainphase.getspan()

    def __print_phase(self,phase,total_time,deepth:int):
        print(f'{repeat("  ",deepth)}{phase.name}: {round(phase.timespan,4)}s {round(phase.timespan * 100 / total_time,4)}%')
        for subphase in phase.subphases:
            self.__print_phase(subphase,total_time,deepth+1)

    def summarize(self):
        total_time = self.get_total_time()
        print(repeat('=',20))
        print('TIME COUSUMING SUMMERY:')
        print(repeat('-',20))
        self.__print_phase(self.mainphase,total_time,0)
        print(repeat('=',20))

global_anlyzer = Analyzer()