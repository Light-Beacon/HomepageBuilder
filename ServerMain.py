'''
服务器主模块
'''
import traceback
import os
import subprocess
import gc
from flask import Flask, request
from Core.project import Project, PageNotFoundError
from Core.io import read_yaml, read_string, write_string
from Core.debug import Logger
from Server.project_updater import request_update

app = Flask(__name__)
logger = Logger('Server')

@app.route("/pull",methods=['POST'])
def git_update():
    '''收到 github 更新信号更新工程文件'''
    status,data = request_update(request,server.project_dir,
        server.config['github_secret'])
    if status == 200:
        server.clear_cache()
    else:
        logger.error(data)
    return data,status

@app.route("/")
def index_page():
    '''默认界面'''
    if server.default_page:
        return getpage(server.default_page)
    else:
        return 'No Page Found',404

@app.route("/<path:alias>")
def getpage(alias:str):
    '''默认页面'''
    if alias.endswith('/version') or alias == 'version':
        return server.get_version()
    while alias.endswith('/'):
        alias = alias[:-1]
    try:
        if alias.endswith('.json'):
            return server.get_page_json(alias[:-5])
        if alias.endswith('.xaml'):
            alias = alias[:-5]
        return server.get_page_xaml(alias)
    except PageNotFoundError:
        return 'No Page Found',404
    except Exception:
        logger.error(traceback.format_exc())
        return 'Inner Error Occured',500

class Server:
    '''服务器类'''
    def __init__(self):
        envpath = os.path.dirname(os.path.dirname(__file__))
        self.config_path = f"{envpath}{os.path.sep}server_config.yml"
        self.version_cache_path = f"{envpath}{os.path.sep}latest_version.cache"
        self.cache = {}
        try:
            self.config = read_yaml(self.config_path)
            self.project_path = self.config['project_path']
            self.project = Project(self.project_path)
            self.default_page = self.project.default_page
            self.project_dir = os.path.dirname(self.project_path)
            self.cache['version'] = self.write_latest_version_cache()
        except Exception as e:
            logger.fatal(e.args)
            exit()

    def clear_cache(self):
        '''清除构建器页面缓存'''
        del self.project
        gc.collect()
        self.project = Project(self.project_path)
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

server = Server()
if __name__ == "__main__":
    app.run(port=6608)
