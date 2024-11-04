from typing import Union, Dict, List
class ReadOnlySetterException(Exception):
    pass

class PropertySetter():
    def __init__(self,fill = None,override = None, frozen = True):
        self.fill:Dict = dict(fill) if fill else {}
        self.override:Dict = dict(override) if override else {}
        self.__frozen = frozen
    
    def attach(self,sticker_setter:Union['PropertySetter', None]):
        """向 Setter 上附上另一层 Setter"""
        if self.__frozen:
            raise ReadOnlySetterException()
        if not sticker_setter:
            return
        self.override.update(sticker_setter.override)
        tempfill = sticker_setter.fill.copy()
        tempfill.update(self.fill)
        self.fill = tempfill
    
    def clone(self):
        new_setter = PropertySetter(self.fill, self.override)
        new_setter.__frozen = False
        return new_setter
    
    def toProperties(self):
        fillcopy = self.fill.copy()
        fillcopy.update(self.override)
        return fillcopy
    
    def decorate(self,property:Dict):
        new_property = self.fill.copy()
        new_property.update(property)
        new_property.update(self.override)
        return new_property
    
    def froze(self):
        self.__frozen = True

    @property
    def isfrozen(self):
        return self.__frozen

    def __len__(self):
        return len(self.fill) + len(self.override)
    
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
    
    def __str__(self) -> str:
        return f'<PS|fill:{self.fill}, override:{self.override}>'