from .FileIO import CreateDict,TryScanDire,ScanSubDire
class Resource:
    def loadResources(self,path:str,prefix:str):
        self.animations.update(CreateDict(TryScanDire(f'{path}\\Animations',r'.*\.xaml$'),prefix))
        self.components.update(CreateDict(TryScanDire(f'{path}\\Components',r'.*\.xaml$'),prefix))
        self.templates.update(CreateDict(TryScanDire(f'{path}\\Templates',r'.*\.yml$'),prefix))
        self.scripts.update(CreateDict(TryScanDire(f'{path}\\Scripts',r'.*\.py$'),prefix))
        self.styles.update(CreateDict(TryScanDire(f'{path}\\Styles',r'.*\.xaml$'),prefix))
        
    def __init__(self):
        self.animations = {}
        self.components = {}
        self.styles = {}
        self.scripts = {}
        self.templates = {}