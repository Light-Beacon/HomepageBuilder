'''
服务器主模块
'''
from flask import Flask, request, make_response
from werkzeug.middleware.proxy_fix import ProxyFix
from ..core.project import PageNotFoundError
from ..core.logger import Logger
from ..core.utils.client import PCLClient
from .project_updater import request_update
from .project_api import ProjectAPI
from ..core.i18n import locale as t
from ..core.config import config, is_debugging

logger = Logger('Server')
app = Flask(__name__)

projapi = None

class Server:
    def __init__(self,project_path=None):
        global projapi
        logger.info(t('server.init'))
        projapi = ProjectAPI(project_path)
        self.limiter = None
        self.init_server_config()

    def init_server_config(self):
        if config('Server.ProxyFix'):
            app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)
        if config('Server.RateLimit.Enable', False):
            from flask_limiter import Limiter
            from flask_limiter.util import get_remote_address
            self.limiter = Limiter(get_remote_address, app = app,
                            default_limits=config('Server.RateLimit.Rate.Default', ["10 per minute"]))

    def run(self,port,flask_debug):
        logger.info(t('server.start',port=port))
        app.run(port=port,debug=flask_debug)

    def get_flask_app(self):
        return app

@app.route("/pull",methods=['POST'])
def git_update():
    '''收到 github 更新信号更新工程文件'''
    if not config('Server.Update.GitHub.Webhook.Enable',False):
        return 'pull not enabled',400
    status,data = request_update(request,projapi.project_dir,
        config('Server.Update.GitHub.Webhook.Secret'))
    if status == 200:
        projapi.reload_project()
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
    args = request.args # 获取参数
    if is_debugging():
        logger.debug(t("server.request.received",page=alias,args=args))
        if realip := request.headers.get('X-Real-IP'):
            logger.debug(f"x_real_ip: {realip}")
    if alias.endswith('/version') or alias == 'version':
        return projapi.get_version(alias,request) # 获取版本号
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
            client = PCLClient.from_request(web_request=request)
            response_dict = projapi.get_page_response(alias, client, args=args)
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


if __name__ == "__main__":
    s = Server()
    s.run(6608)
