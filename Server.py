from flask import Flask, request
from Core.Project import Project
from Core.FileIO import readYaml
from Core.Debug import LogFatal,LogWarning
from Server.project_updater import request_update
import os
import subprocess
app = Flask(__name__)

@app.route("/pull",methods=['POST'])
def git_update():
    status,data = request_update(request,server.project_path,
        server.config['github_secret'])
    if status != 200:
        LogWarning("An Expection occured while updating project: {data}")
    return data,status

@app.route("/<path:name>")
def getpage(name:str):
    LogDebug(f'Requst to access {name}')
    if name.endswith('/version'):
        return server.getPage('version')
    while name.endswith('/'):
        name = name[:-1]
    return server.getPage(name)

class Server: 
    def __init__(self):
        envpath = os.path.dirname(os.path.dirname(__file__))
        self.config_path = f"{envpath}{os.path.sep}server_config.yml"
        self.cache = {}
        try:
            self.config = readYaml(self.config_path)
            self.project_path = self.config['project_path']
            self.project = Project(self.project_path)
            project_dir = os.path.dirname(self.project_path)
            githash = subprocess.check_output('git rev-parse HEAD',cwd = project_dir, shell=True)
            githash = githash.decode("utf-8")
            self.cache['version'] = githash
        except Exception as e:
            LogFatal(e.args)
            exit()
    
    def getPage(self,name):
        if name not in self.cache:
            self.cache[name] = self.project.get_page_xaml(name)
        return self.cache[name]

server = Server()
if __name__ == "__main__":
    app.run(port=6608)