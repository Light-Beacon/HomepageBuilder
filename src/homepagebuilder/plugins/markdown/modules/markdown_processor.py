import re
from abc import ABC
from typing import Annotated, Union, Callable, Optional
from homepagebuilder.core.utils.encode import encode_escape
from homepagebuilder.core.config import config

class PreProcessor(ABC):
    """Markdown 文档预处理器"""
    def process(self, markdown) -> Annotated[str , "Processed markdown document"]:
        """处理 markdown 文档"""
        raise NotImplementedError()

class RegexSubPreProcessor(PreProcessor):
    """使用正则表达式替换的预处理器"""
    def __init__(self, patten: Union[str, re.Pattern], repl: Union[str, Callable[[re.Match],str]], condiction:Optional[Callable] = None):
        self.patten = patten if patten is re.Pattern else re.compile(patten)
        self.repl = repl
        self.condiction = condiction

    def process(self, markdown):
        if self.condiction and not self.condiction(markdown):
            return markdown
        return re.sub(pattern=self.patten, repl=self.repl, string=markdown)

DELETE_LINE_PROCESSOR = RegexSubPreProcessor(
    patten = r'~~(.*?)~~',
    repl = r'<del>\1</del>',
    condiction = lambda _md: not config('markdown.preprocessor.deleteline.disable', False))
"""删除线转义器"""

# 注意：bs4 会将转义字符先反转义一次
BLOCK_CODE_PROCESSOR = RegexSubPreProcessor(
    patten = re.compile(r'`{3,}[\t ]*(\S*)\s*\n(.*?)\n`{3,}', flags=re.RegexFlag.DOTALL),
    repl = lambda matchobj : f'<blockcode lang="{matchobj.group(1).upper()}" code="{encode_escape(matchobj.group(2), with_special=True, with_brace=False)}"/>',
    condiction = lambda _md: not config('markdown.preprocessor.block_codeblock.disable', False))
"""块状代码块转义器"""

WIKI_URL = config('markdown.preprocessor.wikilink.wikiurl', 'https://zh.minecraft.wiki/w/')
WIKI_LINK_PROCESSOR = RegexSubPreProcessor(
    patten = r'\[\[(.*?)\]\]',
    repl = fr'[\1]({WIKI_URL}\1)',
    condiction = lambda _md: not config('markdown.preprocessor.wikilink.disable', False))
"""Wiki 链接代码块转义器"""