from abc import ABC,abstractmethod
from typing import Any, Dict, List, Set, TypedDict, Union
from Core.resource import Resource
from Core.library import Library
from Core.IO import File
from Core.utils import PropertySetter

class Builder(ABC):
    """构建器核心"""
    def __init__(self) -> None:
        self.envpath: str
        self.resources: Resource
        self.template_manager: TemplateManager
        self.current_project: Project
        self.__env:BuildingEnvironment = BuildingEnvironment(
            builder=self
        )

    @abstractmethod
    def load_resources(self,resources_dire_path) -> None:
        """加载构建器资源"""

    @abstractmethod
    def load_modules(self,modules_dire_path) -> None:
        """加载构建器模块"""

    @abstractmethod
    def load_plugins(self, plugin_path) -> None:
        """加载构建器插件"""

    @abstractmethod
    def load_proejct(self,project_path) -> None:
        """加载工程"""

    def get_environment_copy(self) -> 'BuildingEnvironment':
        """获取环境拷贝"""
        return self.__env.copy()


class Project(ABC):
    """工程类接口"""
    @abstractmethod
    def import_pack(self, path:str) -> None:
        """导入工程包"""

    def get_all_card(self) -> list:
        """获取工程里的全部卡片"""
        return self.base_library.get_all_cards()

    def get_all_pagename(self) -> list:
        """获取工程里的全部页面名"""
        return self.pagelist

    def __init__(self,builder, path:str):
        self.builder:Builder = builder
        self.resources:Resource = builder.resources
        self.base_library:Library = None
        self.base_path:str = None
        self.default_page:PageBase = None
        self.version:str = None
        self.pages:Dict[str,PageBase] = {}
        self.pagelist:List[PageBase] = []
        self.__env:'BuildingEnvironment' = builder.get_environment_copy()
        self.__init_env()
        self.import_pack(path)

    @abstractmethod
    def import_page_from_file(self, page_file: File) -> None:
        """导入页面"""

    @abstractmethod
    def get_page_xaml(self, page_alias, no_not_found_err_logging = False, setter = None) -> str:
        """获取页面 xaml 代码"""

    @abstractmethod
    def get_page_content_type(self, page_alias, no_not_found_err_logging = False, setter = None) -> str:
        """获取页面返回类型"""

    @abstractmethod
    def get_page_displayname(self, page_alias) -> str:
        """获取页面显示名"""

    def get_environment_copy(self) -> 'BuildingEnvironment':
        """获取环境拷贝"""
        return self.__env.copy()

    def __init_env(self):
        self.__env.update(project=self)
        self.__env.update(resource=self.resources)
        self.__env.update(animations=self.resources.animations)
        self.__env.update(components=self.resources.components)
        self.__env.update(datas=self.resources.data)
        self.__env.update(page_templates=self.resources.page_templates)
        self.__env.update(templates=self.resources.templates)
        self.__env.update(styles=self.resources.styles)


class BuildingEnvironment(TypedDict):
    """构建时环境"""
    builder: Builder
    """环境构建器"""
    project: Project
    """所在工程"""
    resource: Resource
    """工程资源"""
    animations: Dict[str,str]
    components: Dict[str,str]
    data: Dict[str,object]
    page_templates: Dict[str,str]
    templates: Dict[str,Dict]
    styles: Dict[str,Union[str,Dict]]
    setter: PropertySetter
    used_styles: Set[str]

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        super().update('used_style',Set())

class TemplateManager(ABC):
    '''模版管理器类'''

    @abstractmethod
    def expend_card_placeholders(self,card:Dict,children_code,env):
        '''展开卡片属性内所有占位符'''

    @abstractmethod
    def build_with_template(self,card:Dict,template_name,children_code,env:BuildingEnvironment) -> str:
        '''使用指定模版构建卡片'''

    @abstractmethod
    def packin_containers(self,tree_path:Union[str,List[str]],card:Dict,code:str,env:BuildingEnvironment):
        '''按照容器组件路径包装'''
    
    @abstractmethod
    def build(self,card,env:BuildingEnvironment):
        '''构建卡片'''

class PageBase():
    "页面基类"
    @abstractmethod
    def generate(self, env:BuildingEnvironment):
        "获取页面 XAML 代码"
    
    @property
    def display_name(self):
        raise NotImplementedError()
    
    def get_content_type(self, setter):
        return 'application/xml'