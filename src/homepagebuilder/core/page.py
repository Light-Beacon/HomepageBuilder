from abc import abstractmethod
from typing import TYPE_CHECKING
from .types import Context
from .utils.property import PropertySetter
from .utils.event import set_triggers
from .formatter import format_code
from .logger import Logger
from .i18n import locale as t
from .config import config, is_debugging
from .resource import get_resources_code
from ..debug import global_anlyzer as anl

if TYPE_CHECKING:
    from .types import Context
    from .io import File
    from .utils.client import PCLClient

logger = Logger('Page')

class PageBase():
    "页面基类"
    @abstractmethod
    def generate(self, context:'Context') -> str:
        "获取页面 XAML 代码"
    
    @property
    def display_name(self):
        raise NotImplementedError()
    
    def get_content_type(self, setter:PropertySetter , client:'PCLClient'):
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

class RawXamlPage(FileBasedPage):
    """纯XAML页面"""
    @property
    def display_name(self):
        return self.file.name

    def generate(self, context):
        return self.file.data

class CardStackPage(FileBasedPage):
    """卡片堆叠页面"""
    def __init__(self, file: 'File') -> None:
        super().__init__(file)
        data = file.data
        self.setter = PropertySetter(data.get('fill'), data.get('override'))
        self.name = data.get('name', file.name)
        self.display_name_str = data.get('display_name', self.name)
        self.cardrefs = data.get('cards',{})
        self.alias = data.get('alias', [])

    @property
    def display_name(self):
        return self.display_name_str

    @set_triggers('page.generate')
    def generate(self, context):
        xaml = self.getframe(context)
        #xaml = xaml.replace('${animations}', '')  # TODO
        xaml = xaml.replace('${content}', self.generate_content(context))
        xaml = xaml.replace('${styles}', get_resources_code(context))
        logger.info(t('page.generate.done', page=self.name))
        return xaml

    def generate_content(self, context:'Context'):
        """生成页面主要内容"""
        runtime_setter = self.setter.clone()
        runtime_setter.attach(context.setter)
        content = ''
        for card_ref in self.cardrefs:
            anl.phase(card_ref)
            content += self.__getcardscontent(card_ref, context, setter = runtime_setter)
        return content

    def __getcardscontent(self, ref:str, context:'Context', setter:PropertySetter):
        """一行可能有多个卡片，本方法处理整行"""
        ref = format_code(code=ref, data=setter.toProperties(), context=context)
        code = ''
        for each_card_ref in ref.split(';'):
            code += self.__getonecardcontent(each_card_ref, context, setter.clone())
        return code

    def __getonecardcontent(self, ref, context:Context, setter:PropertySetter):
        """一行可能有多个卡片，本方法处理单个卡片"""
        ref = ref.replace(' ', '').split('|')
        real_ref = ref[0]
        args = ref[1:] if len(ref) > 1 else []
        if real_ref  == '':
            logger.info(t('page.get_card.null'))
            return ''
        setter.attach(PropertySetter.fromargs(args))
        logger.info(t('page.get_card', card_ref=real_ref))
        card = self.__getcard(real_ref,context,setter)
        if not card:
            return ''
        return context.builder.template_manager.build(card,context)

    def __getcard(self,ref,context:Context,setter):
        if is_debugging():
            return self.__getcardunsafe(ref, context, setter)
        try:
            return self.__getcardunsafe(ref, context, setter)
        except Exception as ex:
            logger.warning(t('page.get_card.failed', ex=ex))
            return None 

    def __getcardunsafe(self,ref:str,context:Context,setter):
        card = context.project.base_library.get_card(ref, False)
        card = setter.decorate(card)
        return card

    def getframe(self,context:Context):
        return context.page_templates['Default']