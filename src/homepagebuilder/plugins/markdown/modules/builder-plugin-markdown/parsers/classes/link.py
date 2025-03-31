from enum import Enum
from typing import Union, List
from ..base import InlineNode, InlineNodeContainer
from ..utils import handles

class LinkType(Enum):
    homepage = '打开帮助'
    launch = '启动游戏'
    jrrp = '今日人品'
    rubclean = '清理垃圾'
    ramclean = '内存优化'
    copy = '复制文本'
    refresh_homepage = '刷新主页'
    download = '下载文件'
    browse = '打开网页'

@handles('a')
class Link(InlineNode, InlineNodeContainer):
    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag, *args, **kwargs)
        self.link = self.attrs['href']
        if self.attrs['href'].startswith('pcl:'):
            self.link_type = LinkType[self.attrs['href'].split(':')[1]]
            self.__process_link()
        else:
            self.link_type = LinkType.browse

    def __process_link(self):
        if self.link_type == LinkType.launch:
            self.link = self.link[13:]
            arr = self.link.split('/')
            version = arr[0]
            if version == 'current':
                version = '\\current'
            self.link = version if len(arr) == 1 else f'{version}|{arr[1]}'
        elif self.link_type == LinkType.download:
            self.link = self.link[13:]
        elif self.link_type == LinkType.homepage:
            link = self.link[13:]
            if link.endswith('/'):
                link = link[:-1]
            if not link.endswith('.json'):
                if link.endswith('.xaml'):
                    link = link[:-5] + '.json'
                else:
                    link += '.json'
            self.link = link
        elif self.link_type == LinkType.browse:
            pass
        else:
            self.link = ''

    def get_replacement(self) -> Union[List|None]:
        reps = {'link': self.link, 'type': self.link_type.value}
        ancestor = self.ancestor
        if ancestor.name == 'li':
            reps['pos_down'] = 3
        else:
            reps['pos_down'] = 2
        return reps