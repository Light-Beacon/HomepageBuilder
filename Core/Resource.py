from .FileIO import CreateDict,TryScanDire,ScanSubDire
from .Debug import LogInfo
class Resource:
    def loadResources(self,path:str,prefix:str):
        LogInfo(f'[Resource] Load resource directory: {path}')
        self.animations.update(CreateDict(TryScanDire(f'{path}\\Animations',r'.*\.xaml$'),prefix))
        self.components.update(CreateDict(TryScanDire(f'{path}\\Card_Components',r'.*\.xaml$'),prefix))
        self.components.update(CreateDict(TryScanDire(f'{path}\\Components',r'.*\.xaml$'),prefix))
        self.data.update(CreateDict(TryScanDire(f'{path}\\Data',r'.*'),prefix))
        self.templates.update(CreateDict(TryScanDire(f'{path}\\Card_Templates',r'.*\.yml$'),prefix))
        self.templates.update(CreateDict(TryScanDire(f'{path}\\Templates',r'.*\.yml$'),prefix))
        self.page_templates.update(CreateDict(TryScanDire(f'{path}\\Page_Templates',r'.*\.xaml$'),prefix))
        self.scripts.update(CreateDict(TryScanDire(f'{path}\\Scripts',r'.*\.py$'),prefix))
        self.styles.update(CreateDict(TryScanDire(f'{path}\\Styles',r'.*\.xaml$'),prefix))
        
    def __init__(self):
        self.animations = {}
        self.components = {}
        self.styles = {}
        self.data = {}
        self.scripts = {}
        self.templates = {}
        self.page_templates = {}