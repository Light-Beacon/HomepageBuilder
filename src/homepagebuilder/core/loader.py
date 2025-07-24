import re
from typing import Dict, Union, TypeVar, Optional
from .io import Dire, File
from .logger import Logger
from .elements import Component
from .resource import ResourceLoader
from .config import is_debugging
from .i18n import locale

YAML_PATTERN = re.compile(r'.*\.ya?ml$')
XAML_PATTERN = re.compile(r'.*\.xaml$')
PY_PATTERN = re.compile(r'.*\.py$')

logger = Logger('Loader')

T = TypeVar('T')

class Loader():

    @classmethod
    def load_compoents(cls, direpath) -> Dict[str, Component]:
        return cls.create_structure_mapping(direpath, XAML_PATTERN, Component)

    @classmethod
    def load_tempaltes(cls,direpath) -> Dict[str, Dict]:
        return cls.create_structure_mapping(direpath, YAML_PATTERN)

    @classmethod
    def load_page_tempaltes(cls,direpath) -> Dict[str, str]:
        return cls.create_structure_mapping(direpath, XAML_PATTERN)

    @classmethod
    def load_resources(cls,direpath):
        output = {}
        try:
            dire = Dire(direpath)
        except FileNotFoundError:
            return output
        if is_debugging():
            return cls.__load_resources_unsafe(dire)
        try:
            output = cls.__load_resources_unsafe(dire)
        except Exception as ex:
            logger.error(ex)
            return {}
        return output

    @classmethod
    def __load_resources_unsafe(cls,dire):
        output = {}
        files = dire.scan(patten=YAML_PATTERN,recur=True)
        files.extend(dire.scan(patten=XAML_PATTERN,recur=True))
        output.update(ResourceLoader.loadfiles(files))
        return output

    @classmethod
    def create_structure_mapping(cls,path:str,patten = None,
                                 item_type:Optional[type[T]]=None) -> Dict[str,T]:
        output = {}
        try:
            dire = Dire(path)
            cls.mapping_file(file_or_dire = dire, item_type = item_type,
                        output = output,patten = patten)
        except FileNotFoundError:
            return output
        except Exception as ex:
            logger.error(ex)
            return {}
        return output

    @classmethod
    def mapping_file(cls,file_or_dire,
                     output:Dict[str,object],
                     item_type:Union[type,None]=None,
                     prefix = '',
                     patten = None,
                     is_toplevel:bool = True):
        if isinstance(file_or_dire,File):
            file = file_or_dire
            name = prefix + file.name
            if item_type:
                output[name] = item_type(file=file)
                logger.debug(locale('loader.regist.structure.withtype',type_name=item_type.__name__,name=name))
            else:
                output[name] = file.data
                logger.debug(locale('loader.regist.structure',name=name))
        elif isinstance(file_or_dire,Dire):
            dire = file_or_dire
            for node in dire.scan(patten, include_dires=True):
                cls.mapping_file(node,output,patten=patten,is_toplevel = False, item_type=item_type,
                            prefix = '' if is_toplevel else f'{prefix}{dire.name}/')
        else:
            raise TypeError()