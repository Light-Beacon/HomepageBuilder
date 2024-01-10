from .FileIO import CreateDict,ScanDire,ScanSubDire
class Resource:
    def loadResources(self,path:str,prefix:str):
        self.animations.update(CreateDict(ScanDire(f'{path}\\Animations'),prefix))
        self.components.update(CreateDict(ScanDire(f'{path}\\Components'),prefix))
        self.templates.update(CreateDict(ScanDire(f'{path}\\Templates'),prefix))
        self.scripts.update(CreateDict(ScanDire(f'{path}\\Scripts'),prefix))
        self.styles.update(CreateDict(ScanDire(f'{path}\\Styles'),prefix))
        
    def __init__(self,path):
        self.animations = {}
        self.components = {}
        self.styles = {}
        self.scripts = {}
        self.templates = {}
        self.loadResources('..\\Resources','')
        self.loadResources(f'{path}\\Resources','') # 先读取 PB 自带资源，再更新构建者提供的资源可以实现资源覆盖