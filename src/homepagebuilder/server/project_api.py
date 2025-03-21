import os
import gc
from multiprocessing import Manager
from os.path import sep
from time import time
from ..core.project import Project
from ..core.builder import Builder
from ..core.config import config, is_debugging
from ..core.utils.property import PropertySetter
from ..core.utils.event import set_triggers
from ..core.logger import Logger

manager = Manager()
CROSS_PROCESS_CACHE = None
if config('server.cache.cross', True):
    CROSS_PROCESS_CACHE = manager.dict()

logger = Logger('Server')
VERSION_PROVIDER_CLASSES = {}

class ProjectAPI:
    '''api类'''
    def __init__(self,project_path = None):
        self.cache = {}
        if project_path:
            self.__set_project_path(project_path)
        else:
            raise NotImplementedError()
        try:
            self.builder = Builder()
            self.project = Project(self.builder,self.project_file)
            self.default_page = self.project.default_page
            self.version_provider: VersionProvider = VERSION_PROVIDER_CLASSES.get(
                config('Server.Version.By','time'), VersionProvider)(self)
            self.__run_time_version = 0
            self.trigger_project_update()

        except Exception as e:
            logger.fatal("%s:%s",e.__class__.__name__,e)
            if is_debugging():
                raise e
            exit()

    def __set_project_path(self,path):
        if os.path.isdir(path):
            self.project_file = f"{path}{sep}Project.yml"
            self.project_dir  = path
        else:
            self.project_file = path
            self.project_dir  = os.path.dirname(path)

    @set_triggers('server.project.reload')
    def reload_project(self):
        '''重载工程'''
        del self.project
        gc.collect()
        self.project = Project(self.builder,self.project_file)
        self.cache.clear()
        self.trigger_project_update()
        logger.info('[Server] Project Reloaded.')

    def trigger_project_update(self):
        ''' 触发 project 更新信号'''
        self.__run_time_version += 1
        if CROSS_PROCESS_CACHE:
            CROSS_PROCESS_CACHE['project.version'] = self.__run_time_version

    def __check_project_update(self):
        if CROSS_PROCESS_CACHE:
            version = CROSS_PROCESS_CACHE.get('project.version')
            if version > self.__run_time_version:
                self.reload_project()

    @set_triggers('server.get.version')
    def get_version(self,alias,request):
        '''获取主页版本'''
        self.__check_project_update()
        if self.version_getter.require_request:
            return self.version_getter.get_page_version(alias,request)
        if ('__version', alias) not in self.cache:
            self.cache[('__version', alias)] = self.version_getter.get_page_version(alias,request)
        return self.cache[('__version', alias)]

    def get_page_json(self,alias):
        '''获取页面json文件'''
        self.__check_project_update()
        key = alias + '.json'
        if key not in self.cache:
            name = self.project.get_page_displayname(alias)
            if name is None:
                name = alias
            self.cache[key] = name
        return {'response': f'{{"Title":"{self.cache[key]}"}}',
                'content-type': 'application/json'}

    @set_triggers('server.get.page')
    def get_page_response(self,alias,client,args = None):
        '''获取页面内容'''
        self.__check_project_update()
        if (alias,args) not in self.cache:
            setter = PropertySetter(None,args,False)
            if len(setter) > 0:
                setter.attach(client.getsetter())
                return self.get_response_dict(alias,setter,client)
            else:
                if rsp := self.cache.get((alias,client.pclver)):
                    return rsp
                else:
                    setter.attach(client.getsetter())
                    self.cache[(alias,client.pclver)] = self.get_response_dict(alias,setter,client)
                    return self.cache[(alias,client.pclver)]

    def get_response_dict(self,alias,setter,client):
        setter.attach(client.getsetter())
        return {'response':self.project.get_page_xaml(alias,setter=setter),
                'content-type' : self.project.get_page_content_type(alias,setter=setter) }

class VersionProvider():
    '''
    用于实现版本号获取的类
    ## 用法
    继承该类，指定 `name`，并实现 `get_page_version` 方法'''

    name:str = None
    '''名称'''

    require_request: bool = False
    '''标识版本是否与请求内容有关'''

    api: ProjectAPI
    '''项目 API'''

    def __init__(self,api):
        self.api = api

    @classmethod
    def get_page_version(self, alias :str, request):
        """
        获取页面版本号
        ### 参数
        * `alias` 待获取的页面路径
        * `request` 获取版本号时时发送的 HTTP 请求
            * 如需使用本项，请将派生类的 `require_request` 设置为 `True` 以禁用版本号缓存
        """
        raise NotImplementedError()

    def __init_subclass__(cls, **kwargs):
        if name := cls.name:
            VERSION_PROVIDER_CLASSES[name] = cls
        else:
            raise ValueError()

class VersionTimeProvider(VersionProvider):
    name = 'time'
    @classmethod
    def get_page_version(self, _alias :str, _request):
        return str(time())

class VersionStaticProvider(VersionProvider):
    name = 'static'
    @classmethod
    def get_page_version(self, _alias :str, _request):
        return str(config('Server.Version.StaticValue'))
