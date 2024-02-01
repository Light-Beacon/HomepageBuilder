from .FileIO import readYaml,ScanDire,ScanSubDire
from .Library import Library
from .Resource import Resource
from .Templates_Manager import TemplateManager
from .Debug import Log
import os

class Project:
    def load_plugins(self,plugin_path):
        for data,name,exten in ScanSubDire(plugin_path,'pack\.yml'):
            dire = os.path.dirname(data['file_path'])
            self.resources.loadResources(f'{dire}\\Resources','')
            
    def import_pack(self,path):
        Log(f'[Project] Start to import pack {path}')
        pack_info = readYaml(path)
        self.version = pack_info['version']
        Log(f'[Project] Pack version: {self.version}')
        self.base_path = os.path.dirname(path)
        Log(f'[Project] Loading cards')
        self.base_library = Library(readYaml(f"{self.base_path}\\Libraries\\library.yml"))
        Log(f'[Project] Importing resources')
        self.resources.loadResources(f'{self.base_path}\\Resources','')
        Log(f'[Project] Loading pages')
        for pair in ScanDire(f'{self.base_path}\\Pages',r'.*\.yml$'):
            page:dict = pair[0]
            self.pages.update({ page['name']:page })
            if 'alias' in page:
                for alias in page.get('alias'):
                    self.pages.update({ alias:page })
        
    def __init__(self,path):
        envpath = os.path.dirname(os.path.dirname(__file__))
        self.resources = Resource()
        Log(f'[Project] Loading basic resources')
        self.resources.loadResources(f'{envpath}\\Resources','')
        Log(f'[Project] Loading plugins')
        self.load_plugins(f'{envpath}\\Plugin')
        self.pages = {}
        self.import_pack(path)
        self.TemplateManager = TemplateManager(self.resources)
        Log(f'[Project] Loaded pack completely!')
    
    def get_page_xaml(self,page_alias):
        if page_alias not in self.pages:
            # TODO PAGE NOT FOUND EXCEPTION
            pass
        xaml = ''
        for card_ref in self.pages[page_alias]['cards']:
            card_ref = card_ref.replace(' ','').split('|')
            card = self.base_library.getCard(card_ref[0],False)
            if len(card_ref) > 1:
                for arg in card_ref[1:]:
                    cardarg = arg.split('=')
                    card[cardarg[0]] = cardarg[1]
            card_xaml = self.TemplateManager.build(card)
            #card_xaml = format_code(card_xaml,card,self.resources.scripts)
            xaml += card_xaml
        return xaml