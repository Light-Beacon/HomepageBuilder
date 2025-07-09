import markdown
from bs4 import BeautifulSoup
from homepagebuilder.interfaces import script, require
from homepagebuilder.core.config import config
from homepagebuilder.interfaces import Logger

parsers_module = require('markdown_parsers')
processor_module = require('markdown_processor')
create_node = parsers_module.create_node
logger = Logger('MarkdownPresenter')
class MarkdownPresenter:
    def __init__(self):
        self.pre_process_pipeline = []
        if not config('markdown.preprocessor.deleteline.disable', False): 
            self.add_pre_processor(processor_module.DELETE_LINE_PROCESSOR)
        if not config('markdown.preprocessor.block_codeblock.disable', False): 
            self.add_pre_processor(processor_module.BLOCK_CODE_PROCESSOR)
        if not config('markdown.preprocessor.wikilink.disable', False): 
            self.add_pre_processor(processor_module.WIKI_LINK_PROCESSOR)
    
    def add_pre_processor(self, processor):
        self.pre_process_pipeline.append(processor)
    
    def pre_process(self, markdown:str) -> str:
        for processor in self.pre_process_pipeline:
            markdown = processor.process(markdown)
        return markdown
    
    def html2xaml(self, html, context):
        '''html转为xaml代码'''
        soup = BeautifulSoup(html,'html.parser')
        xaml = ''
        for tag in soup.find_all(recursive=False):
            xaml += create_node(tag,context,[]).convert()
        return xaml

    def convert(self, md,context):
        '''生成xaml代码'''
        md = self.pre_process(md)
        html = markdown.markdown(md)
        logger.noisy(f'Converted markdown to html: {html}')
        xaml = self.html2xaml(html,context)
        return xaml

mdp_singleton = MarkdownPresenter()

@script('MarkdownPresenter')
def markdown_presenter(card,context,**_):
    '''从markdown生成xaml代码脚本'''
    md = card['markdown']   
    return mdp_singleton.convert(md,context)