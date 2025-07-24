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
    def __init__(self, major, minor = 0, micro = 0, detail = None):
        self.major = major
        self.minor = minor
        self.micro = micro
        self.detail = detail

    @classmethod
    def from_string(cls, version_str):
        major, minor, micro, *detail = version_str.split(".")
        return cls(major, minor, micro, detail)

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.micro}{'.' + '.'.join(map(str, self.detail)) if self.detail else ''}"

    def __repr__(self):
        return f"{self.major}.{self.minor}.{self.micro}{'.' + '.'.join(map(str, self.detail)) if self.detail else ''}"

    def __rt__(self, other):
        if other is ...:
            return True
        return (self.major, self.minor, self.micro) > (other.major, other.minor, other.micro)

    def __lt__(self, other):
        if other is ...:
            return True
        return (self.major, self.minor, self.micro) < (other.major, other.minor, other.micro)

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
            return True
        return (self.major, self.minor) > (other.major, other.minor)

    @classmethod
    def builder_version(cls):
        return cls.from_string(importlib.metadata.version("homepagebuilder"))
