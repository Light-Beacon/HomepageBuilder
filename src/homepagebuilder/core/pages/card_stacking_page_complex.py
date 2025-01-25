from .bases import FileBasedPage
from ..types.context import Context
from typing import TYPE_CHECKING, Dict, List
if TYPE_CHECKING:
    from ..types import Context
    from ..io import File

class NewCardStackPage(FileBasedPage):
    """新版卡片堆叠页面"""
    def __init__(self, file: 'File') -> None:
        super().__init__(file)
        data = file.data
        self.cards: List = []
        self.name = data.get('name', file.name)
        self.display_name = data.get('display_name', self.name)
        self.alias = data.get('alias', [])
        self.accept_args = []

    def __import(self, attr, source):
        setattr(self, attr, source)

    def generate(self, context:Context):
        xaml = ''
        context = context.copy()
        context.page = Fomatter.format(self.todict(), context)
        for card in self.cards:
            xaml += card.generate(context)
            
    
    @property
    def alias(self):
        return self.env.get('alias', [])
    
    @property
    def display_name(self):
        return self.env.get('display_name', self.name)

    def todict(self):
        return self.env.copy().update({
            "name": self.name,
            "display_name": self.display_name,
            "alias": self.alias,
            "accept_args": self.accept_args,
            "cards": self.cards
        })

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