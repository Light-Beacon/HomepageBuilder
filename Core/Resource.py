from .FileIO import CreateDict,TryScanDire,ScanSubDire
from .Debug import LogInfo
from os.path import sep
class Resource:
    def loadResources(self,path:str,prefix:str):
        LogInfo(f'[Resource] Loading resource pack: {path}')
        self.animations.update(CreateDict(TryScanDire(f'{path}{sep}Animations',r'.*\.xaml$'),prefix))
        self.components.update(CreateDict(TryScanDire(f'{path}{sep}Card_Components',r'.*\.xaml$'),prefix))
        self.components.update(CreateDict(TryScanDire(f'{path}{sep}Components',r'.*\.xaml$'),prefix))
        self.data.update(CreateDict(TryScanDire(f'{path}{sep}Data',r'.*'),prefix))
        self.templates.update(CreateDict(TryScanDire(f'{path}{sep}Card_Templates',r'.*\.yml$'),prefix))
        self.templates.update(CreateDict(TryScanDire(f'{path}{sep}Templates',r'.*\.yml$'),prefix))
        self.page_templates.update(CreateDict(TryScanDire(f'{path}{sep}Page_Templates',r'.*\.xaml$'),prefix))
        self.scripts.update(CreateDict(TryScanDire(f'{path}{sep}Scripts',r'.*\.py$'),prefix))
        self.styles.update(CreateDict(TryScanDire(f'{path}{sep}Styles',r'.*\.xaml$'),prefix))
        self.styles.update(CreateDict(TryScanDire(f'{path}{sep}Styles',r'.*\.yml$'),prefix))
        
    def __init__(self):
        self.animations = {}
        self.components = {}
        self.styles = {}
        self.data = {}
        self.scripts = {}
        self.templates = {}
        self.page_templates = {}