"""
版本号实现
"""

from typing import TYPE_CHECKING
from time import time
import hashlib
from ...core.config import config, is_debugging
from ...core.logger import Logger
from ...core.utils.property import PropertySetter

logger = Logger('VersionProvider')

VERSION_PROVIDER_CLASSES = {}
if TYPE_CHECKING:
    from ..project_api import ProjectAPI

def get_provider_class() -> type['VersionProvider']:
    """
    获取当前配置使用的 Provider 类
    """
    provider_name = config('Server.Version.By','time')
    if provider_class := VERSION_PROVIDER_CLASSES.get(provider_name.lower()):
        return provider_class
    else:
        if is_debugging():
            logger.error('Version provider: "%s" is invalid. Supported providers: %s',
                        provider_name, str.join(',',VERSION_PROVIDER_CLASSES.keys()))
            raise KeyError(provider_name)
        else:
            logger.warning('Version provider: "%s" is invalid. Supported providers: %s',
                        provider_name, str.join(',',VERSION_PROVIDER_CLASSES.keys()))
            return VersionTimeProvider

class VersionProvider():
    '''
    用于实现版本号获取的类
    ## 用法
    继承该类，指定 `name`，并实现 `get_page_version` 方法'''

    name:str = None
    '''名称'''

    dynamic: bool = False
    '''标识版本是否与请求内容有关'''

    api: 'ProjectAPI'
    '''项目 API'''

    def __init__(self,api):
        self.api = api

    def get_page_version(self, alias:str, request):
        """
        获取页面版本号
        ### 参数
        * `alias` 待获取的页面路径
        * `request` 获取版本号时时发送的 HTTP 请求
            * 如需使用本项，请将派生类的 `dynamic` 设置为 `True` 以禁用版本号缓存
        """
        raise NotImplementedError()

    def __init_subclass__(cls, **kwargs):
        if name := cls.name:
            VERSION_PROVIDER_CLASSES[name] = cls
        else:
            raise ValueError()

class VersionTimeProvider(VersionProvider):
    name = 'time'

    def get_page_version(self, _alias :str, _request):
        return str(time())

class VersionStaticProvider(VersionProvider):
    name = 'static'

    def get_page_version(self, _alias :str, _request):
        return str(config('Server.Version.Static.Value'))

class VersionHashProvider(VersionProvider):
    name = 'hash'
    hash_method:str = None

    def __init__(self, api):
        super().__init__(api)
        self.hash_method = config('Server.Version.Hash.Method', 'MD5')


    def get_hash(self) -> str:
        """获取哈希

        Raises:
            ValueError: 当调试状态下 hash_mathod 不受支持时引起该错误

        Returns:
            str: 16进制哈希
        """
        page_result = self.api.get_page_xaml(self.api.default_page, PropertySetter()).encode()
        hash_object = None
        match self.hash_method.upper():
            case 'MD5':
                hash_object = hashlib.md5(page_result)
            case 'SHA1':
                hash_object = hashlib.sha1(page_result)
            case 'SHA256':
                hash_object = hashlib.sha256(page_result)
            case _:
                if is_debugging():
                    logger.error('Hash method: "%s" is invalid. Supported hash mothods: MD5, SHA1, SHA256',
                                   self.hash_method)
                    raise ValueError(self.hash_method)
                else:
                    logger.warning('Hash method: "%s" is invalid. Supported hash mothods: MD5, SHA1, SHA256',
                                   self.hash_method)
                    hash_object = hashlib.md5(page_result)
        return hash_object.hexdigest()

    def get_page_version(self, _alias :str, _request):
        return self.get_hash()
