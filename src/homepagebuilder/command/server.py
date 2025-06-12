import os
from .proc import CommandProcesser
from ..core.i18n import locale as t

DEFALUT_PORT = 6608

class ServerCommand(CommandProcesser):
    name = 'server'
    help = t('command.server.help')

    def init_subparser(self,parser):
        parser.add_argument('--project', type=str,
                            default=os.getcwd() + os.path.sep + 'Project.yml',
                            help=t('command.server.help.args.project'))
        parser.add_argument('-p', '--port', type=str,
                            help=t('command.server.help.args.port'))
        parser.add_argument('--flask-debug', action='store_true',
                            help=t('command.server.help.args.flask_debug'))

    def process(self,args):
        from ..server.main import Server
        server = Server(args.project)
        server.run(args.port if args.port else DEFALUT_PORT,
                   flask_debug = args.flask_debug or False)
