from typing import Union, Dict, List
class ReadOnlySetterException(Exception):
    pass

class PropertySetter():
    def __init__(self,fill = None,override = None):
        self.fill:Dict = fill if fill else {}
        self.override:Dict = override if override else {}
        self.frozen = True
    
    def attach(self,sticker_setter:Union['PropertySetter', None]):
        if self.frozen:
            raise ReadOnlySetterException()
        if not sticker_setter:
            return
        self.override.update(sticker_setter.override)
        tempfill = sticker_setter.fill.copy()
        tempfill.update(self.fill)
        self.fill = tempfill
    
    def clone(self):
        new_setter = PropertySetter(self.fill, self.override)
        new_setter.frozen = False
        return new_setter
    
    def toProperties(self):
        fillcopy = self.fill.copy()
        fillcopy.update(self.override)
        return fillcopy
    
    @classmethod
    def fromargs(cls,args:List[str]):
        override = {}
        for arg in args:
            if '=' in arg:
                argname, argvalue = arg.split('=')
                override[argname] = argvalue
            else:
                override[argname] = False if argname.startswith('!') else True
        return PropertySetter(None,override)