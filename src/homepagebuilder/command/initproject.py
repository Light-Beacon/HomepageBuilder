import importlib.resources as pkg_resources
import shutil
import os
from .proc import CommandProcesser

class FolderNotEmptyError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class InitProjectCommand(CommandProcesser):
    name = 'initproject'
    help = 'Creat a new project by using template'

    def init_subpraser(self,parser):
        parser.add_argument('template', nargs="?", default='default',
                            help='name of the template')
        parser.add_argument('--location', type=str,
                              default=os.getcwd(),
                              help='project path')

    def process(self,args):
        try:
            copy_installed_package_folder(args.template, args.location)
        except FileNotFoundError as e:
            print(f'Project template "{args.template}" Not Exist!')
            raise e


def copy_installed_package_folder(folder_name, dest_folder):
    package_path = pkg_resources.files('homepagebuilder')
    src_folder = package_path / 'projects'/ folder_name

    if not os.path.exists(src_folder):
        raise FileNotFoundError(src_folder)

    if bool(os.listdir(dest_folder)):
        print('The folder is not empty! Creating a new proejct may damage your files!')
        for _ in range(3):
            inputstr = input('Do you still want to creat a new project in this folder? [y/n] ')
            if inputstr.lower() in ['y', 'yes' ,'true' ,'oui' ,'si' ,'是']:
                break
            if inputstr.lower() in ['n', 'no' ,'false' ,'non' ,'否']:
                raise FolderNotEmptyError(dest_folder)
            print('Input Incorrect. Please input "yes" or "no".')
        else:
            print('Max retry times reached. Creating canceled.')
            raise FolderNotEmptyError(dest_folder)

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True)
    print(f'Created a new project with template "{folder_name}"')
