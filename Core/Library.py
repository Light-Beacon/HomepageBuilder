'''
该模块内存放了卡片库类
'''
import os
from typing import Tuple
from .io import scan_dire,scan_sub_dire
from .debug import log_info,log_error

class Library:
    '''卡片库类'''
    def __init__(self,data:dict):
        self.name= data['name']
        log_info(f'[Library] Loading library: {self.name}')
        self.fill = data.get('fill',{})
        self.cover = data.get('cover',{})
        self.card_mapping = {}  # 卡片索引
        self.libs_mapping = {}  # 子库索引
        self.sub_libraries = {} # 子库
        self.cards = {}
        self.location = os.path.dirname(data['file_path'])
        for file_tuple in scan_dire(self.location,r'^(?!^__LIBRARY__.yml$).*$'):  # 库所拥有的卡片
            self.add_card_from_file_tuple(file_tuple)
        self.add_sub_libraries(scan_sub_dire(self.location,'__LIBRARY__.yml'))  # 遍历添加子库

    @classmethod
    def decorate_card(cls,card,fill,cover):
        '''用 fill 和 cover 修饰卡片'''
        if fill:
            cloned_fill = fill.copy()
        else:
            cloned_fill = {}
        if cover:
            card.update(cover)
        cloned_fill.update(card)
        return cloned_fill

    def __decorate_card(self,card):
        '''用本卡片库的 fill 和 cover 修饰卡片'''
        return self.decorate_card(card,self.fill,self.cover)

    def __get_card_decoless(self,card_ref:str,is_original:bool):
        '''获取未经 fill 和 cover 的卡片'''
        if card_ref in self.cards:
            return self.cards[card_ref]
        if ':' in card_ref:
            libname,cardname = card_ref.split(':',2)
            if libname == self.name:
                card_ref = cardname
            else:
                return self.get_card_from_lib_mapping(libname,cardname,is_original)
        return self.get_card_from_card_mapping(card_ref,is_original)

    def get_card(self,card_ref:str,is_original:bool):
        '''获取卡片'''
        target = self.__get_card_decoless(card_ref,is_original)
        if is_original:
            return target
        else:
            return self.__decorate_card(target)

    def get_card_from_card_mapping(self,card_ref:str,is_original:bool):
        '''通过库内的卡片映射获取卡片'''
        if card_ref in self.cards:
            return self.cards[card_ref].copy()
        elif card_ref in self.card_mapping:
            return self.card_mapping[card_ref].getCard(card_ref,is_original)
        else:
            raise KeyError(log_error(f'[Library] Cannot find card "{card_ref}"'))

    def get_card_from_lib_mapping(self,lib_name,card_ref,is_original):
        '''通过库内的库映射获取卡片'''
        if lib_name == 'T':
            return {'templates':[card_ref]}
        if lib_name in self.libs_mapping:
            return self.libs_mapping[lib_name].getCard(card_ref,is_original)
        else:
            raise KeyError(log_error(f'[Library] Cannot find library "{card_ref}"'))

    def add_card_from_file_tuple(self,file_info_tuple:Tuple[object,str,str]):
        '''通过文件元组添加卡片'''
        data, filename, exten = file_info_tuple
        name = filename
        if isinstance(data,dict):
            if 'name' in data:
                name = data['name']
            self.cards[name] = data
        else:
            self.cards[name] = {'data':data }
        self.cards[name].update({'data':data,'file_name':filename,'file_exten':exten,
                                 'card_id':f'{self.name}:{name}','card_lib':self.name,
                                 'card_name':name})

    def add_sub_libraries(self,yamldata):
        '''增加子库'''
        def add_sub_library(self,yamldata):
            sublib = Library(yamldata)
            self.sub_libraries.update({sublib.name:sublib})
            # 将子库的卡片索引加入父库并映射到该子库
            for cardname in sublib.card_mapping:
                self.card_mapping.update({cardname:sublib})
            # 将子库的所有卡片加入父库并映射到该子库
            for cardname in sublib.cards:
                self.card_mapping.update({cardname:sublib})
            # 将子库的子库引加入父库并映射到该子库
            for libname in sublib.libs_mapping:
                self.libs_mapping.update({libname:sublib})
            # 将该子库加入父库的子库索引
            self.libs_mapping.update({sublib.name:sublib})
        if isinstance(yamldata,list):
            for data in yamldata:
                self.add_sub_libraries(data)
        elif isinstance(yamldata,tuple):
            add_sub_library(self,yamldata[0])
        else:
            add_sub_library(self,yamldata)
        # DEV NOTICE 如果映射的内存占用太大了就将每一个卡片和每一个子库的路径压成栈，交给根库来管理

    def get_all_cards(self):
        '''获取该库的所有卡片'''
        result = [self.__decorate_card(card) for card in self.cards.values()]
        for lib in self.sub_libraries.values():
            result += [self.__decorate_card(card) for card in lib.get_all_cards()]
        return result
