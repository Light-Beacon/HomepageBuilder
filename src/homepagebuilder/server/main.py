'''
服务器主模块
'''
from flask import Flask, request, make_response
from typing import Tuple, Union
from ..core.project import PageNotFoundError
from ..core.logger import Logger
from .project_updater import request_update
from .project_api import ProjectAPI
from ..core.utils.property import PropertySetter
from ..core.i18n import locale as t
from ..core.config import config

logger = Logger('Server')
app = Flask(__name__)
projapi = None

class Server:
    def __init__(self,project_path=None):
        global projapi
        logger.info(t('server.init'))
        projapi = ProjectAPI(project_path)

    def run(self,port):
        logger.info(t('server.start',port=port))
        app.run(port=port)

    def get_flask_app(self):
        return app

@app.route("/pull",methods=['POST'])
def git_update():
    '''收到 github 更新信号更新工程文件'''
    if not config('process.update.github',False):
        return 'pull not enabled',400
    status,data = request_update(request,projapi.project_dir,
        config('server.update.github.webhook.secret'))
    if status == 200:
        projapi.clear_cache()
    else:
        logger.error(data)
    return data,status

@app.route("/")
def index_page():
    '''默认界面'''
    if projapi.default_page:
        return getpage(projapi.default_page)
    else:
        return 'No Page Found',404




@app.route("/<path:alias>")
def getpage(alias:str):
    '''默认页面'''
    if alias.endswith('/version') or alias == 'version':
        return projapi.get_version() # 获取版本号
    args = request.args # 获取参数
    logger.debug(t("server.request.received",page=alias,args=args))
    while alias.endswith('/'):
        alias = alias[:-1]
    mode = None
    if alias.endswith('.json'):
        mode = 'json'
        alias = alias[:-5] # 这里两个都得保留
    elif alias.endswith('.xaml'):
        mode = 'xaml'
        alias = alias[:-5] # 这里两个都得保留
    try:
        if mode == 'json':
            response_dict = projapi.get_page_json(alias)
            logger.debug(t("server.request.response.json",page=alias,args=args))
        else:
            response_dict = projapi.get_page_response(alias,client=ClientArgs(request),args=args)
            logger.debug(t("server.request.response.page",page=alias,args=args))
        response = make_response(response_dict['response'])
        response.headers['Content-Type'] = response_dict['content-type']
        return response
    except PageNotFoundError:
        logger.debug(t("server.request.response.not_found",page=alias,args=args))
        return process_not_found(alias,mode)
    except Exception as e:
        logger.error(t("server.request.response.error",page=alias,args=args))
        logger.exception(e)
        if mode == 'json':
            return process_err_page_json(500)
        else:
            return 'Inner Error Occured',500

def process_not_found(alias,mode):
    '''处理页面未找到的请求'''
    if mode == 'json':
        return process_err_page_json(404)
    if alias == 'could_you_buy_me_a_coffee':
        return 'Sure You Need A Coffee And I AM A TEAPOT',418
    return 'No Page Found',404

def process_err_page_json(err_code):
    '''处理发生错误的 JSON 请求'''
    return f'{{"Title":"{err_code}"}}'

class ClientArgs:
    def __init__(self,web_request):
        self.is_pcl, self.is_open = self.__getpcltype(web_request=web_request)
        self.pclver = self.__getpclver(web_request=web_request)
        self.pclver_id = self.__getpclverid(web_request=web_request)

    def __getpcltype(self,web_request) -> Tuple[bool,Union[bool|None]]:
        refer = web_request.headers.get('Referer','')
        if refer.endswith('pcl2.server/'):
            return True, False
        if refer.endswith('pcl2.open.server/'):
            return True, True
        return False, None
    
    def __getpclverid(self,web_request):
        refer = web_request.headers.get('Referer','')
        if not self.is_pcl:
            return None
        return int(refer[7:10])

    def __getpclver(self,web_request):
        uas = web_request.headers.get('User-Agent','')
        uas = uas.split()
        if len(uas) >= 1:
            if pclver := uas[0].split('/'):
                if pclver[0] == 'PCL2':
                    return pclver[1]
        return None
    
    def getsetter(self):
        d = {
            'client':{
                'is-pcl': self.is_pcl,
                'is-open': self.is_open,
                'version': self.pclver,
                'version-id': self.pclver_id
            }
        }
        return PropertySetter(override=d)


if __name__ == "__main__":
    s = Server()
    s.run(6608)
