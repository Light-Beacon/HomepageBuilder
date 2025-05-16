import os
import gc
from multiprocessing import Manager
from os.path import sep
from ..core.project import Project
from ..core.builder import Builder
from ..core.config import config, is_debugging
from ..core.utils.property import PropertySetter
from ..core.utils.client import PCLClient
from ..core.utils.event import set_triggers
from ..core.logger import Logger
from .utils.version_providers import VersionProvider, get_provider_class

manager = Manager()
CROSS_PROCESS_CACHE = None
if config('server.cache.cross', True):
    CROSS_PROCESS_CACHE = manager.dict()

logger = Logger('Server')

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
            self.version_provider: VersionProvider = get_provider_class()(self)
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
        self.clear_cache()
        self.trigger_project_update()
        logger.info('[Server] Project Reloaded.')

    def clear_cache(self):
        '''清除缓存'''
        self.cache.clear()
        logger.info('Cache cleared.')

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
    def get_version(self, alias, request):
        '''获取主页版本'''
        self.__check_project_update()
        if self.version_provider.dynamic:
            return self.version_provider.get_page_version(alias,request)
        if ('__$version', alias) not in self.cache:
            self.cache[('__$version', alias)] = self.version_provider.get_page_version(alias,request)
        return self.cache[('__$version', alias)]

    @set_triggers('server.get.json')
    def get_page_json(self, alias):
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
    def get_page_response(self,alias, client:PCLClient, args = None):
        '''获取页面内容'''
        self.__check_project_update()
        setter = PropertySetter(None, args, False)
        if len(setter) > 0:
            return self.get_response_dict(alias, setter, client)
        client_hash = hash(client)
        if not (rsp := self.cache.get((alias, client_hash))):
            rsp = self.get_response_dict(alias,setter,client)
            self.cache[(alias, client_hash)] = rsp
        return rsp

    def get_response_dict(self,alias, setter, client):
        return {'response':self.project.get_page_xaml(alias, setter=setter, client=client),
                'content-type' : self.project.get_page_content_type(alias, setter=setter, client=client) }

    def get_page_xaml(self, alias, setter):
        return self.project.get_page_xaml(alias, setter=setter)
