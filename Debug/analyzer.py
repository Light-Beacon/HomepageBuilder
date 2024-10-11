
import time
from typing import List

def repet(string,times:int):
    s = ''
    for _ in range(0,times):
        s += string
    return s
    

class Phase():
    def __init__(self,name):
        self.name = name
        self.__timespan = 0
        self.__start_time = None
        self.__end_time = None
        self.__pasued = False

    @property
    def timespan(self):
        if not self.__start_time:
            raise PhaseNotStartedError(phase = self)
        return self.__timespan
    
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
        self.__end_time = time.time()
        self.__timespan += self.__getspan(self.__end_time)

    def is_ended(self):
        return bool(self.__end_time)
    
    def __checklock(self):
        if self.__end_time:
            raise PhaseEndedError(phase = self)

    def __getspan(self, curtime = time.time()):
        return curtime - self.__start_time

class PhaseNotStartedError(Exception):
    pass

class PhaseStartedError(Exception):
    pass

class PhaseEndedError(Exception):
    pass


class Analyzer():
    def __init__(self) -> None:
        self.currentphase = None
        self.phaselist:List[Phase] = []

    def phase(self,name) -> Phase:
        '''阶段'''
        self.stop()
        self.currentphase = Phase(name)
        self.phaselist.append(self.currentphase)
        self.currentphase.start()
    
    def stop(self):
        if self.currentphase and not self.currentphase.is_ended():
            self.currentphase.stop()

    def summarize(self):
        print(repet('=',10))
        print('Running Summary:')
        print(repet('-',10))
        for phase in self.phaselist:
            print(f'{phase.name} : Consumed {round(phase.timespan,4)}s')
        print(repet('=',10))

global_anlyzer = Analyzer()