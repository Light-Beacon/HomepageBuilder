import re
from abc import ABC
from typing import Annotated, Union, Callable
from homepagebuilder.core.utils.encode import encode_escape
from homepagebuilder.core.config import config

class PreProcessor(ABC):
    """Markdown 文档预处理器"""
    def process(self, markdown) -> Annotated[str , "Processed markdown document"]:
        """处理 markdown 文档"""

class RegexSubPreProcessor(PreProcessor):
    """使用正则表达式替换的预处理器"""
    def __init__(self, patten: Union[str, re.Pattern], repl: Union[str, Callable[[re.Match],str]]):
        self.patten = patten if patten is re.Pattern else re.compile(patten)
        self.repl = repl
    
    def process(self, markdown):
        return re.sub(pattern=self.patten, repl=self.repl, string=markdown)
    
DELETE_LINE_PROCESSOR = RegexSubPreProcessor(
    patten = r'~~(.*?)~~',
    repl = r'<del>\1</del>')
"""删除线转义器"""

# 注意：bs4 会将转义字符先反转义一次
BLOCK_CODE_PROCESSOR = RegexSubPreProcessor(
    patten = re.compile(r'`{3,}[\t ]*(\S*)\s*\n(.*?)\n`{3,}', flags=re.RegexFlag.DOTALL),
    repl = lambda matchobj : f'<blockcode lang="{matchobj.group(1).upper()}" code="{encode_escape(matchobj.group(2), with_special=True)}"/>')
"""块状代码块转义器"""

WIKI_URL = config('markdown.preprocessor.wikilink.wikiurl', 'https://zh.minecraft.wiki/w/')
WIKI_LINK_PROCESSOR = RegexSubPreProcessor(
    patten = r'\[\[(.*?)\]\]',
    repl = fr'[\1]({WIKI_URL}\1)')
"""Wiki 链接代码块转义器"""