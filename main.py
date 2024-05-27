'''构建器主入口'''
import argparse
from Core.project import Project
from Core import config

def command_build(args):
    project = Project(args.project_file_path)
    if args.page:
        page = args.page
    else:
        page = project.default_page
    xaml = project.get_page_xaml(page)
    filepath = args.output_path
    with open(filepath,'w',encoding='utf-8') as f:
        f.write(xaml)

def command_server(args):
    from Server.main import Server
    server = Server(args.project_path)
    server.run(args.port if args.port else 6608)

command_func_mapping = {
    'build': command_build,
    'server': command_server
}

def main():
    '''构建器主入口'''
    parser = argparse.ArgumentParser()
    command = 's'
    subparsers = parser.add_subparsers(help='Command',dest='command')
    parser_build = subparsers.add_parser('build', help='Build homepage')
    parser_server = subparsers.add_parser('server', help='Start server')

    parser_build.add_argument('project_file_path', type=str, help='project file path')
    parser_build.add_argument('output_path', type=str, help='generated file dest')
    parser_build.add_argument('-p','--page', type=str, help='page name')

    parser_server.add_argument('project_path', type=str, help='project path')
    parser_server.add_argument('-p','--port', type=str, help='project path')
    args = parser.parse_args()

    command_func_mapping[args.command](args)

if __name__ == '__main__':
    config.fully_init()
    main()
