from typing import Union, Dict, List
class ReadOnlySetterException(Exception):
    pass

class PropertySetter():
    def __init__(self,default = None,override = None, frozen = True):
        self.default:Dict = dict(default) if default else {}
        self.override:Dict = dict(override) if override else {}
        self.__frozen = frozen

    @classmethod
    def create_empty_setter(cls) -> 'PropertySetter':
        """创建一个空的 PropertySetter"""
        return cls({}, {})

    def attach(self,sticker_setter:Union['PropertySetter', None]):
        """向 Setter 上附上另一层 Setter"""
        if self.__frozen:
            raise ReadOnlySetterException()
        if not sticker_setter:
            return
        self.override.update(sticker_setter.override)
        temp_default = sticker_setter.default.copy()
        temp_default.update(self.default)
        self.default = temp_default

    def clone(self):
        new_setter = PropertySetter(self.default, self.override, False)
        return new_setter

    def toProperties(self):
        default_copy = self.default.copy()
        default_copy.update(self.override)
        return default_copy

    def decorate(self,property:Dict):
        new_property = self.default.copy()
        new_property.update(property)
        new_property.update(self.override)
        return new_property

    def froze(self):
        self.__frozen = True

    @property
    def isfrozen(self):
        return self.__frozen

    def __len__(self):
        return len(self.default) + len(self.override)

    @classmethod
    def fromargs(cls,args:List[str]):
        override = {}
        for arg in args:
            if '=' in arg:
                argname, argvalue = arg.split('=')
                override[argname] = argvalue
            else:
                override[arg] = False if arg.startswith('!') else True
        return PropertySetter(None,override)

    def __str__(self) -> str:
        return f'<PS|default:{self.default}, override:{self.override}>'
