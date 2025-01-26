'''
该模块内存放了卡片库类
'''
import os
from enum import IntEnum
from .io import Dire,File
from .logger import Logger
from .i18n import locale as t
from .utils.event import set_triggers
from .utils.property import PropertySetter

logger = Logger('Library')

class IndexingOption(IntEnum):
    public = 7
    """正常加入上一级索引"""
    protect_sub = 6
    """子库不加入上一级索引"""
    protect_file = 5
    """库内文件不加入上一级索引"""
    private = 4
    """子库与库内文件均不加入上一级索引"""
    ignore = 0
    """子库本身以及所有子内容均不加入索引"""
    
    @classmethod
    def indexing_sublibs(cls, option: 'IndexingOption'):
        return bool(option.value & 1)
    
    @classmethod
    def indexing_subfiles(cls, option: 'IndexingOption'):
        return bool(option.value & 2)
    
    @classmethod
    def indexing_self(cls, option: 'IndexingOption'):
        return bool(option.value & 4)

class Library:
    '''卡片库类'''
    @set_triggers('library.init')
    def __init__(self,data:dict):
        self.name= data['name']
        logger.info(t('library.load',name=self.name))
        self.setter = PropertySetter(data.get('fill'),data.get('override'))
        self.setter.override.update(data.get('cover',{})) # 兼容性考虑
        self.indexing = IndexingOption[data.get('indexing', 'public').lower()]
        self.card_mapping = {}  # 卡片索引
        self.libs_mapping = {}  # 子库索引
        self.sub_libraries = {} # 子库
        self.cards = {}
        self.dire = Dire(os.path.dirname(data['file_path']))
        for file in self.dire.scan(patten=r'^(?!^__LIBRARY__.yml$).*$'):  # 库所拥有的卡片
            self.add_card_from_file(file)
        self.add_sub_libraries(self.dire.scan_subdir('__LIBRARY__.yml'))  # 遍历添加子库

    def __get_decoless_card(self,card_ref:str,is_original:bool):
        '''获取未经本库修饰的卡片'''
        if card := self.cards.get(card_ref):
            return card
        libname = None
        if ':' in card_ref:
            libname, card_ref = card_ref.split(':',2)
        return self.get_card_from_mapping(card_ref,libname,is_original)

    @set_triggers('library.getcard')
    def get_card(self,card_ref:str,is_original:bool):
        '''获取卡片'''
        target = self.__get_decoless_card(card_ref,is_original)
        if is_original:
            return target
        else:
            return self.setter.decorate(target)

    def get_card_from_mapping(self,card_ref,lib_name,is_original):
        '''通过库内的映射获取卡片'''
        if lib_name: # 如果指定子库
            if lib_name == self.name:
                return self.cards[card_ref]
            if lib_name == 'T':
                return {'templates':[card_ref]}
            targetlib = self.libs_mapping.get(lib_name)
            if not targetlib:
                exp = KeyError(f'[Library] Cannot find library "{lib_name}"')
                logger.exception(exp)
                raise exp
            return targetlib.get_card(lib_name + ':' + card_ref,is_original)
        else:
            if card_ref in self.cards:
                return self.cards[card_ref].copy()
            targetlib = self.card_mapping.get(card_ref)
            if not targetlib:
                exp = KeyError(f'[Library] Cannot find card "{card_ref} among sub-libraries"')
                logger.exception(exp)
                raise exp
            return targetlib.get_card(card_ref,is_original)

    @set_triggers('library.creatcard.fromfile')
    def add_card_from_file(self,file:File):
        '''通过文件添加卡片'''
        filename = file.name
        exten = file.extention
        data = file.data
        name = filename
        if isinstance(data,dict):
            if 'name' in data:
                name = data['name']
            self.cards[name] = data
        else:
            self.cards[name] = {'data':data }
        self.cards[name].update({'data':data,'file_name':filename,'file_exten':exten,
                                 'card_id':f'{self.name}:{name}','card_lib':self.name,
                                 'card_name':name,'file': file})
        return self.cards[name]

    @set_triggers('library.subs.add')
    def add_sub_libraries(self,files):
        '''增加子库'''
        def add_sub_library(self,yamldata):
            sublib = Library(yamldata)
            self.sub_libraries.update({sublib.name:sublib})
            if IndexingOption.indexing_subfiles(self.indexing):
                # 将子库的文件索引加入父库并映射到该子库
                for cardname in sublib.card_mapping:
                    self.card_mapping[cardname] = sublib
                # 将子库的所有文件加入父库并映射到该子库
                for cardname in sublib.cards:
                    self.card_mapping.update({cardname:sublib})
            if IndexingOption.indexing_sublibs(self.indexing):
                # 将子库的子库引加入父库并映射到该子库
                for libname in sublib.libs_mapping:
                    self.libs_mapping.update({libname:sublib})
            if IndexingOption.indexing_self(self.indexing):
                # 将该子库加入父库的子库索引
                self.libs_mapping.update({sublib.name:sublib})
        if isinstance(files,list):
            for file in files:
                self.add_sub_libraries(file)
        elif isinstance(files,File):
            add_sub_library(self,files.data)
        else:
            add_sub_library(self,files)
        # DEV NOTICE 如果映射的内存占用太大了就将每一个文件和每一个子库的路径压成栈，交给根库来管理

    @set_triggers('library.getallcard')
    def get_all_cards(self):
        '''获取该库的所有卡片'''
        result = [self.setter.decorate(card) for card in self.cards.values()]
        for lib in self.sub_libraries.values():
            result += [self.setter.decorate(card) for card in lib.get_all_cards()]
        return result

    def get_library(self,name):
        if name in self.sub_libraries:
            return self.sub_libraries[name]
        if nextlib := self.libs_mapping.get(name):
            return nextlib.get_library(name)
        else:
            raise LibraryNotFoundError()

class LibraryNotFoundError(Exception):
    """页面未找到错误"""