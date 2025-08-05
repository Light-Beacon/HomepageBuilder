import os
from os import makedirs
from os.path import sep, exists
from pathlib import Path
from typing import TYPE_CHECKING
from .proc import CommandProcesser
from ..core.logger import Logger
from ..core.i18n import locale as t

if TYPE_CHECKING:
    from ..core.builder import Builder
    from ..core.project import Project
    from ..core.page import PageBase

logger = Logger('Command|Build')

class BuildCommand(CommandProcesser):
    """构建命令处理类"""
    name = 'build'
    help = t('command.build.help')

    def init_subparser(self, parser):
        parser.add_argument('--project', type=str,
                            default=Path(os.getcwd()) / 'Project.yml',
                            help=t('command.build.help.args.project'))
        parser.add_argument('--output-path', type=str, default=None,
                            help=t('command.build.help.args.output'))
        parser.add_argument('-p', '--page', type=str,
                            help=t('command.build.help.args.page'))
        parser.add_argument('-a', '--all-page', action='store_true',
                            help=t('command.build.help.args.all_page'))
        parser.add_argument('--dry-run', action='store_true',
                            help=t('command.build.help.args.dry_run'))
        parser.add_argument('--not-pcl', action='store_true',
                            help=t('command.build.help.args.not_pcl'))
        parser.add_argument('--pcl-is-opensource',action='store_true',
                            help=t('command.build.help.args.pcl_is_opensource'))
        parser.add_argument('--pcl-versionid', type=int, default=None,
                            help=t('command.build.help.args.pcl_versionid'))

    def process(self, args) -> None:
        from ..core.builder import Builder
        builder = Builder()
        project_path = Path(args.project)
        try:
            builder.load_project(project_path)
        except FileNotFoundError as e:
            logger.critical("%s: %s", t('command.build.failed'), ', '.join(e.args))
            raise SystemExit(1) from e
        if args.all_page:
            self.__gen_allpage(args,builder,args.output_path)
        else:
            page = args.page
            self.__gen_single_page(args, page, builder, args.output_path)

    def __gen_single_page(self, args, page, builder, page_output_path):
        if not page_output_path:
            page_output_path = os.getcwd() + os.path.sep + 'output.xaml'
        if not page:
            page = builder.current_project.default_page
        if args.dry_run:
            page_output_path = None
        self.__build_and_output(builder.current_project, page, page_output_path, args)
        logger.info(t('command.build.done', path=page_output_path))

    def __gen_allpage(self, args, builder: 'Builder', path):
        if not path:
            path = os.getcwd() + os.path.sep + 'output' + os.path.sep
        if not path.endswith(sep):
            path = path + sep
        if not exists(path) and not args.dry_run:
            makedirs(path, exist_ok=True)
        for page in builder.current_project.get_all_page():
            page_output_path = f"{path}{page.id}.xaml"
            self.__gen_single_page(args,page,builder,page_output_path)

    @classmethod
    def __build_and_output(cls, project:'Project', page:'PageBase', output_path, args):
        xaml = project.get_page_xaml(page=page)
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(xaml)
