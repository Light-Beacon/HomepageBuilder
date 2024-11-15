import os
from os import makedirs
from os.path import sep, exists
from .proc import CommandProcesser
from ..core.utils.property import PropertySetter
class BuildCommand(CommandProcesser):
    name = 'build'
    help = 'Build Homepage'

    def init_subpraser(self,parser):
        parser.add_argument('--project', type=str,
                              default=os.getcwd() + os.path.sep + 'Project.yml',
                              help='project file path')
        parser.add_argument('--output-path', type=str,
                              default= os.getcwd() + os.path.sep + 'output.xaml',
                              help='generated file dest')
        parser.add_argument('-p', '--page', type=str, help='page name')
        parser.add_argument('-a', '--all-page', action='store_true', help='generate all page')
        parser.add_argument('--dry-run', action='store_true', help='dry run')
        parser.add_argument('--not-pcl', action='store_true')
        parser.add_argument('--pcl-opensource', action='store_true')
        parser.add_argument('--pcl-versionid', type=int, default=None, help='PCL version')

    def process(self,args) -> None:
        from ..core.builder import Builder
        builder = Builder()
        builder.load_proejct(args.project)
        output_path = args.output_path
        if args.all_page:
            if not exists(args.output_path):
                makedirs(args.output_path, exist_ok=True)
            for page in builder.current_project.get_all_pagename():
                if not args.output_path.endswith(sep):
                    output_path = output_path + sep
                if args.dry_run:
                    page_output_path = None
                else:
                    page_output_path = f"{output_path}{page}.xaml"
                self.build_and_output(builder.current_project, page, page_output_path, args)
        else:
            page = args.page
            if not page:
                page = builder.current_project.default_page
            if args.dry_run:
                page_output_path = None
            else:
                page_output_path = f"{output_path}"
            self.build_and_output(builder.current_project, page, page_output_path, args)

    @classmethod
    def build_and_output(cls,project, page, output_path, args):
        xaml = project.get_page_xaml(page_alias=page,setter = PropertySetter(override={
                'client':{
                    'ispcl': not args.not_pcl,
                    'isopensource': args.pcl_opensource,
                    'versionid': args.pcl_versionid
                }
            }))
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(xaml)