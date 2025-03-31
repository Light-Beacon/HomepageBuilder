import markdown
from bs4 import BeautifulSoup
from homepagebuilder.interfaces import script
from homepagebuilder.core.config import config
from .parsers.utils import create_node_from_tag
from . import processor as processors

class MarkdownPresenter:
    def __init__(self):
        self.pre_process_pipeline = []
        if not config('markdown.preprocessor.deleteline.disable', False): 
            self.add_pre_processor(processors.DeleteLinePreProcessor)
        if not config('markdown.preprocessor.block_codeblock.disable', False): 
            self.add_pre_processor(processors.BlockCodePreProcessor)
        if not config('markdown.preprocessor.wikilink.disable', False): 
            self.add_pre_processor(processors.WikiLinkPreProcessor)

    def add_pre_processor(self, processor: processors.PreProcessor):
        """添加预处理器

        Args:
            processor (PreProcessor): 继承于 PreProcessor 的处理器类型
        """
        self.pre_process_pipeline.append(processor)

    def pre_process(self, content:str) -> str:
        for processor in self.pre_process_pipeline:
            content = processor.process(content)
        return content

    def html2xaml(self, html, context):
        '''html转为xaml代码'''
        soup = BeautifulSoup(html,'html.parser')
        xaml = ''
        for tag in soup.find_all(recursive=False):
            xaml += create_node_from_tag(tag = tag,
                                         context = context,
                                         parent_stack=[]).convert()
        return xaml

    def convert(self, md,context):
        '''生成xaml代码'''
        md = self.pre_process(md)
        html = markdown.markdown(md)
        xaml = self.html2xaml(html,context)
        return xaml

mdp_singleton = MarkdownPresenter()

@script('MarkdownPresenter')
def markdown_presenter(card,context,**_):
    '''从markdown生成xaml代码脚本'''
    md = card['markdown']   
    return mdp_singleton.convert(md,context)
