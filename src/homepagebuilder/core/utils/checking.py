"""类型检查限制模块"""
from typing import TYPE_CHECKING
import importlib.metadata

if TYPE_CHECKING:
    from ..io import File

def is_xaml(file:'File') -> bool:
    "判断文件是否为Xaml"
    return file.extention == 'xaml'

def is_yaml(file:'File') -> bool:
    "判断文件是否为Yaml"
    return file.extention in ['yml','yaml']

class Version():
    """版本号"""
    def __init__(self, major:int, minor:int = 0, micro:int = 0, detail = None):
        if not (isinstance(major, int) and isinstance(minor, int) and isinstance(micro, int)):
            raise TypeError()
        self.major = major
        self.minor = minor
        self.micro = micro
        self.detail = detail

    @classmethod
    def from_string(cls, version_str:str):
        version_seq = [0,0,0]
        sub_version_list = version_str.split(".")
        for i in range(min(3, len(sub_version_list))):
            sub_version = sub_version_list[i]
            if sub_version.isdecimal():
                version_seq[i] = int(sub_version)
            else:
                break
        else:
            i += 1
        detail = sub_version_list[i:]
        return cls(version_seq[0], version_seq[1], version_seq[2], detail)

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.micro}{'.' + '.'.join(map(str, self.detail)) if self.detail else ''}"

    def __repr__(self):
        return f"{self.major}.{self.minor}.{self.micro}{'.' + '.'.join(map(str, self.detail)) if self.detail else ''}"

    def __gt__(self, other):
        if other is ...:
            return True
        return (self.major, self.minor, self.micro) > (other.major, other.minor, other.micro)

    def __lt__(self, other):
        if other is ...:
            return True
        return (self.major, self.minor, self.micro) < (other.major, other.minor, other.micro)

    def __ge__(self, other):
        if other is ...:
            return True
        return (self.major, self.minor, self.micro) >= (other.major, other.minor, other.micro)
    
    def __le__(self, other):
        if other is ...:
            return True
        return (self.major, self.minor, self.micro) <= (other.major, other.minor, other.micro)
    
    def __eq__(self, other):
        if other is ...:
            return True
        return (self.major, self.minor, self.micro) == (other.major, other.minor, other.micro)

    def __lshift__(self, other):
        if other is ...:
            return True
        return (self.major, self.minor) < (other.major, other.minor)

    def __rshift__(self, other):
        if other is ...:
            return False
        return (self.major, self.minor) > (other.major, other.minor)

    @classmethod
    def builder_version(cls):
        return cls.from_string(importlib.metadata.version("homepagebuilder"))
