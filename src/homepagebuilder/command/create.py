import importlib.resources as pkg_resources
import shutil
import os
from .proc import CommandProcesser
from ..core.i18n import locale as t
from ..core.utils.checking import Version

class FolderNotEmptyError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class CreateProjectCommand(CommandProcesser):
    name = 'create'
    help = t('command.create.help')

    def init_subparser(self,parser):
        parser.add_argument('template', nargs="?", default='default',
                            help=t('command.create.help.args.template'))
        parser.add_argument('--location', type=str,
                              default=os.getcwd(),
                              help=t('command.create.help.args.location'))

    def __copy_installed_package_folder(self, folder_name, dest_folder):
        package_path = pkg_resources.files('homepagebuilder')
        src_folder = package_path / 'projects'/ folder_name

        if not os.path.exists(src_folder):
            raise FileNotFoundError(src_folder)

        if bool(os.listdir(dest_folder)):
            print(t('command.create.folder_not_empty'))
            for _ in range(3):
                inputstr = input(t('command.create.folder_not_empty.confirm'))
                if inputstr.lower() in ['y', 'yes' ,'true' ,'oui' ,'si' ,'是']:
                    break
                if inputstr.lower() in ['n', 'no' ,'false' ,'non' ,'否']:
                    raise FolderNotEmptyError(dest_folder)
                print(t('command.create.folder_not_empty.input_error'))
            else:
                print(t('command.create.folder_not_empty.max_retry'))
                raise FolderNotEmptyError(dest_folder)

        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

        shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True)

        with open(os.path.join(dest_folder, 'Project.yml'), 'a', encoding='utf-8') as f:
            f.write('\nversion: ' + str(Version.builder_version()) + '\n')

        print(t('command.create.created', template=folder_name))

    def process(self,args):
        try:
            self.__copy_installed_package_folder(args.template, args.location)
        except FileNotFoundError as e:
            print(t('command.create.template_not_exist', template=args.template))
            raise e
