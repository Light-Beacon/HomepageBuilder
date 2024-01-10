from .FileIO import ReadYaml, ScanDireReadYaml
from .Library import Library
from .Code_Formatter import format_code
from .Templates_Manager import TemplateManager
import os

class Project:
    def __init__(self,path):
        data = ReadYaml(path)
        self.version = data['version']
        self.base_path = os.path.dirname(path)
        self.base_library = Library(f"{base_path}\\Libraries\\library.yaml")
        self.pages = {}
        self.elements = {} # TODO
        self.presenters = {} # TODO
        # 注册 Presenter 附带的元素
        for p in presenters.values():
            self.elements.update(p.plugin_elements)
        self.TemplateManager = TemplateManager(self.elements,self.presenterss)
        self.TemplateManager.load(f'{base_path}\\Templates')
        for pair in ScanDireReadYaml(f'{base_path}\\Pages'):
            page = pair[1]
            pages.update({ page['name']:page })
            for alias in page['alias']:
                pages.update({ alias:page })
    
    def get_page_xaml(self,page_alias):
        if page_alias not in self.pages.keys():
            # TODO PAGE NOT FOUND EXCEPTION
            pass
        xaml = ''
        for card_ref in self.pages[page_alias]['cards']:
            card = base_library.getCard(card_ref)
            card_xaml = self.TemplateManager.build(card)
            card_xaml = format_code(card_xaml,card,self.scripts)
            xaml += card_xaml
        return xaml