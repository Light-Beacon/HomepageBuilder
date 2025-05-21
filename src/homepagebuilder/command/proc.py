from argparse import ArgumentParser
class CommandProcesser:
    """命令处理类"""

    name: str
    """命令的执行名称"""
    help: str
    """命令的帮助文档"""

    def __init__(self,subparsers) -> None:
        if not self.name:
            raise NotImplementedError()
        self.parser:ArgumentParser = subparsers.add_parser(self.name, help=self.help)
        self.__common_init_subpraser(self.parser)
        self.init_subpraser(self.parser)

    def __common_init_subpraser(self,parser):
        parser.add_argument('--debug', help='enable debug mode', action='store_true')
        parser.add_argument('--logging-level', type=int, help='set logging level')

    def init_subpraser(self,parser:ArgumentParser):
        """初始化解析器"""
        raise NotImplementedError()

    def process(self,args) -> None:
        """处理指令"""
        raise NotImplementedError
