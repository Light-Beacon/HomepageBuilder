from abc import ABC,abstractmethod
from typing import Dict, List, TYPE_CHECKING


if TYPE_CHECKING:
    from . import Builder, Context
    from ..resource import Resource
    from ..library import Library
    from ..io import File
    from ..page import PageBase

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
        self.__context:'Context' = builder.get_context_copy()
        self.__context.project = self
        self.base_library:Library = None
        self.base_path:str = None
        self.default_page:str = None
        self.version:str = None
        self.pages:Dict[str,PageBase] = {}
        self.pagelist:List[PageBase] = []
        self.import_pack(path)

    @abstractmethod
    def import_page_from_file(self, page_file: 'File') -> None:
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

    def get_context_copy(self) -> 'Context':
        """获取环境拷贝"""
        return self.__context.copy(self.__context)
