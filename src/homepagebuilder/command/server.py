import os
from pathlib import Path
from .proc import CommandProcessor
from ..core.i18n import locale as t

DEFAULT_PORT = 6608

class ServerCommand(CommandProcessor):
    """服务器命令处理类"""
    name = 'server'
    help = t('command.server.help')

    def init_subparser(self, parser):
        parser.add_argument('--project', type=str,
                            default=Path(os.getcwd()) / 'Project.yml',
                            help=t('command.server.help.args.project'))
        parser.add_argument('--host', type=str,
                            help=t('command.server.help.args.host'))
        parser.add_argument('-p', '--port', type=str,
                            help=t('command.server.help.args.port'))
        parser.add_argument('--flask-debug', action='store_true',
                            help=t('command.server.help.args.flask_debug'))

    def process(self, args):
        from ..server.main import Server
        server = Server(args.project)
        server.run(
            args.host if args.host else '127.0.0.1',
            args.port if args.port else DEFAULT_PORT,
            flask_debug = args.flask_debug or False)
