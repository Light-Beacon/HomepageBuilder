'''
资源结构模块
'''
import re
from abc import ABC, abstractmethod
from typing import Dict, Annotated, List
from .io import File
from .logger import Logger
from .utils.checking import is_xaml, is_yaml
from .i18n import locale
import xml.etree.ElementTree as ET

logger = Logger('Resource')
YML_PATTERN = re.compile(r'.*\.yml$')
XAML_PATTERN = re.compile(r'.*\.xaml$')
PY_PATTERN = re.compile(r'.*\.py$')

XML_ROOT = '''
<Root
xmlns:pb="lr-namespace:PageBuilder"
xmlns:sys="clr-namespace:System;assembly=mscorlib"
xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
xmlns:local="clr-namespace:PCL;assembly=Plain Craft Launcher 2">
{chindren}
</Root>
'''

class ResourceLoader:

    @classmethod
    def loadfiles(cls,files):
        output = {}
        for file in files:
            resources = cls.loadfile(file)
            for _key,resource in resources.items():
                output[resource.key] = resource
        return output

    @classmethod
    def loadfile(cls,file:File) -> List['Resource']:
        logger.debug(locale('resourceloader.load.resourcefile',name=file.name))
        if is_xaml(file):
            return cls.__loadxamlfile(file)
        elif is_yaml(file):
            return cls.__loadyamlfile(file)
        else:
            raise ValueError()
    
    @classmethod
    def __loadyamlfile(cls,file:Annotated[File,is_yaml]):
        """加载yaml资源文件"""
        output = {}
        data:Dict = file.data
        if styles := data.get('Styles'):
            for style in styles:
                res = StyleResource(style)
                output[res.key] = res
                logger.debug(locale('resourceloader.load.regist',name=res.key,type_name=res.type))
        return output

    @classmethod
    def __loadxamlfile(cls,file:Annotated[File,is_xaml]):
        """加载xaml资源文件"""
        output = {}
        data = XML_ROOT.replace('{chindren}', file.data)
        root = ET.fromstring(data)
        for element in root:
            res = XamlResource(element)
            output[res.key] = res
            logger.debug(locale('resourceloader.load.regist',name=res.key,type_name=res.type))
        return output

class Resource(ABC):
    """资源基类"""
    key:str

    @abstractmethod
    def getxaml(self):
        "获取xaml"

    @property
    @abstractmethod
    def type(self):
        """资源类型"""

class StyleResource(Resource):
    setters: Dict[str,object]
    is_default_style: bool

    def __init__(self,style_dict):
        super().__init__()
        self.setters = {}
        self.target = style_dict.get('Target')
        if key := style_dict.get('Key'):
            self.is_default_style = False
            self.key = key
        else:
            self.is_default_style = True
            self.key = f'Default/{self.target}'
        if setters := style_dict.get('setters'):
            for property_name,value in setters.items():
                self.setters[property_name] = value

    @property
    def type(self):
        return 'Style'

    def getxaml(self):
        xaml = '<Style '
        if not self.is_default_style:
            xaml += f'x:Key="{self.key}" '
        xaml += f'TargetType={self.target}>'
        for property_name,value in self.setters.items():
            xaml += f'<Setter Property="{property_name}" Value="{value}"/>'
        xaml += '</Style>\n'
        return xaml

class XamlResource(Resource):
    is_default: bool

    def __init__(self,element):
        self.target = element.get('TargetType')
        self.__type = element.tag
        if key := element.get('{http://schemas.microsoft.com/winfx/2006/xaml}Key'):
            self.is_default = False
            self.key = key
        else:
            self.is_default = True
            if self.target:
                self.key = f'Default/{self.target}'
            else:
                raise ValueError()
        self.xaml = ET.tostring(element)

    @property
    def type(self):
        return self.__type

    def getxaml(self):
        return self.xaml