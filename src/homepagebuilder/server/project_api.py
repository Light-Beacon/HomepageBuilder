import os
import subprocess
import gc
from os.path import sep as sep
from ..core.project import Project
from ..core.builder import Builder
from ..core.io import read_string, write_string
from ..core.config import is_debugging
from ..core.utils.property import PropertySetter
from ..core.logger import Logger


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
            self.version_cache_path = f"{self.project_dir}{sep}cache{sep}latest_version.cache"
            self.default_page = self.project.default_page
            self.cache['version'] = self.write_latest_version_cache()
        except Exception as e:
            logger.fatal(e.args)
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

    def clear_cache(self):
        '''清除构建器页面缓存'''
        del self.project
        gc.collect()
        self.project = Project(self.project_file)
        self.cache.clear()
        self.write_latest_version_cache()
        logger.info('[Server] Cache cleared.')

    def get_latest_version_cache(self):
        '''获取最新的主页版本字符串缓存'''
        return read_string(self.version_cache_path)

    def write_latest_version_cache(self):
        ''' 将 commit hash 写入缓存并返回其值 '''
        version_hash = self.get_githash()
        write_string(self.version_cache_path,version_hash)
        return version_hash

    def get_githash(self):
        '''获取 commit hash'''
        githash = subprocess.check_output('git rev-parse HEAD',cwd = self.project_dir, shell=True)
        return githash.decode("utf-8")

    def get_version(self):
        '''获取主页版本'''
        if 'version' not in self.cache:
            self.cache['version'] = self.get_githash()
        latest_version = self.get_latest_version_cache()
        if self.cache['version'] != latest_version:
            self.clear_cache()
            self.cache['version'] = self.get_githash()
        return self.cache['version']

    def get_page_json(self,alias):
        '''获取页面json文件'''
        key = alias + '.json'
        if key not in self.cache:
            name = self.project.get_page_displayname(alias)
            if name is None:
                name = alias
            self.cache[key] = name
        return {'response': f'{{"Title":"{self.cache[key]}"}}',
                'content-type': 'application/json'}

    def get_page_response(self,alias,client,args = None):
        '''获取页面内容'''
        if (alias,args) not in self.cache:
            setter = PropertySetter(None,args)
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