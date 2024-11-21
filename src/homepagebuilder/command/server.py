import os
from .proc import CommandProcesser

DEFALUT_PORT = 6608

class ServerCommand(CommandProcesser):
    name = 'server'
    help = 'Run server'

    def init_subpraser(self,parser):
        parser.add_argument('--project', type=str,
                            default=os.getcwd() + os.path.sep + 'Project.yml',
                            help='project file path')
        parser.add_argument('-p', '--port', type=str, help='project path')
        parser.add_argument('--flask-debug', action='store_true')

    def process(self,args):
        from ..server.main import Server
        server = Server(args.project)
        server.run(args.port if args.port else DEFALUT_PORT,
                   flask_debug = args.flask_debug or False)
