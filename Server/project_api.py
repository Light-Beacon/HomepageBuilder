import os
import subprocess
import gc
from Core.project import Project
from Core.io import read_yaml, read_string, write_string
from Core.debug import Logger
from os.path import sep as sep

logger = Logger('Server')

class ProjectAPI:
    '''api类'''
    def __init__(self,project_path = None):
        self.cache = {}
        if project_path:
            self.__set_project_path(project_path)
            self.config_path = f"{self.project_dir}{sep}Config{sep}server_config.yml"
            self.config = read_yaml(self.config_path)
        else:
            envpath = os.path.dirname(os.path.dirname(__file__))
            self.config_path = f"{envpath}{os.path.sep}server_config.yml"
            self.config = read_yaml(self.config_path)
            project_path = self.config['project_path']
            self.__set_project_path(project_path)
        try:
            self.project = Project(self.project_file)
            self.version_cache_path = f"{self.project_dir}{sep}Cache{sep}latest_version.cache"
            self.default_page = self.project.default_page
            self.cache['version'] = self.write_latest_version_cache()
        except Exception as e:
            logger.fatal(e.args)
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
        return f'{{"Title":"{self.cache[key]}"}}'

    def get_page_xaml(self,alias):
        '''获取页面xaml文件'''
        if alias not in self.cache:
            self.cache[alias] = self.project.get_page_xaml(alias)
        return self.cache[alias]
