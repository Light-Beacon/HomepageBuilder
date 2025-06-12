from argparse import ArgumentParser
from ..core.i18n import locale as t

class CommandProcesser:
    """命令处理类"""

    name: str
    """命令的执行名称"""
    help: str
    """命令的帮助文档"""

    def __init__(self,subparsers) -> None:
        if not self.name:
            raise NotImplementedError()
        self.parser:ArgumentParser = subparsers.add_parser(self.name, help=self.help, add_help=False)
        self.__common_init_subparser(self.parser)
        self.init_subparser(self.parser)

    def __common_init_subparser(self,parser):
        parser.add_argument('-h', '--help', action='help', help=t('command.help'))
        parser.add_argument('--debug', help=t('command.help.debug'), action='store_true')
        parser.add_argument('--logging-level', type=int, help=t('command.help.logging_level'))

    def init_subparser(self,parser:ArgumentParser):
        """初始化解析器"""
        raise NotImplementedError()

    def process(self,args) -> None:
        """处理指令"""
        raise NotImplementedError
