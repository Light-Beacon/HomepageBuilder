from abc import abstractmethod
from typing import TYPE_CHECKING
from ..types import Context
from ..utils.property import PropertySetter

if TYPE_CHECKING:
    from ..types import Context
    from ..io import File

class PageBase():
    "页面基类"
    @abstractmethod
    def generate(self, context:'Context'):
        "获取页面 XAML 代码"
    
    @property
    def display_name(self):
        raise NotImplementedError()
    
    def get_content_type(self, setter:PropertySetter):
        return 'application/xml'

class FileBasedPage(PageBase):
    "基于文件的页面，仅应用于继承"
    def __init__(self, file: 'File') -> None:
        super().__init__()
        self.file = file

class CodeBasedPage(PageBase):
    "基于代码的页面，仅应用于继承"
    def __init__(self, project) -> None:
        super().__init__()
        self.project = project