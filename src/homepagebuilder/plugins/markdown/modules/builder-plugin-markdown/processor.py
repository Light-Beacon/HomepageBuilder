import re
from abc import ABC
from typing import Annotated, Union, Callable
from homepagebuilder.core.utils.encode import encode_escape
from homepagebuilder.core.config import config

class PreProcessor(ABC):
    """Markdown 文档预处理器"""
    @classmethod
    def process(cls, markdown:str) -> Annotated[str , "Processed markdown document"]:
        """处理 markdown 文档"""

class RegexSubPreProcessor(PreProcessor):
    """使用正则表达式替换的预处理器"""
    patten: Union[str, re.Pattern]
    repl: Union[str, Callable[[re.Match],str]]

    def __init__(self):
        raise NotImplementedError

    @classmethod
    def process(cls, markdown):
        return re.sub(pattern=cls.patten, repl=cls.repl, string=markdown)

class DeleteLinePreProcessor(RegexSubPreProcessor):
    """删除线转义器"""
    patten = r'~~(.*)~~'
    repl = r'<del>\1</del>'

# 注意：bs4 会将转义字符先反转义一次
class BlockCodePreProcessor(RegexSubPreProcessor):
    """块状代码块转义器"""
    patten = re.compile(r'`{3,}[\t ]*(\S*)\s*\n(.*?)\n`{3,}', flags=re.RegexFlag.DOTALL)
    repl = lambda matchobj : f'<blockcode lang="{matchobj.group(1).upper()}" code="{encode_escape(matchobj.group(2), with_special=True)}"/>'


WIKI_URL = config('markdown.preprocessor.wikilink.wikiurl',
                  'https://zh.minecraft.wiki/w/')

class WikiLinkPreProcessor(RegexSubPreProcessor):
    """Wiki 链接代码块转义器"""
    patten = r'\[\[(.*?)\]\]',
    repl = fr'[\1]({WIKI_URL}\1)'
