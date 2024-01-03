from .yaml import EnumDire, ScanDireRead
import os

class Library:
    def __init__(self,data):
        self.name= data['name']
        self.fill = data['fill']
        self.cover = data['cover']
        self.card_mapping = {}  # 卡片索引
        self.libs_mapping = {}  # 子库索引
        self.sub_libraries = {} # 子库
        self.location = os.path.dirname(data['path'])
        self.cards = ScanDireRead(self.location,r'^(?!library\.yaml$).*i')  # 库所拥有的卡片
        self.add_sub_libraries(EnumDire(self.location,'library.yaml'))  # 遍历添加子库

    def decorateCard(self,card):
        # 用 fill 和 cover 修饰卡片
        cloned_fill = self.fill.copy()
        card.update(self.cover)
        cloned_fill.update(card)
        return cloned_fill
    
    def getCard(self,card_ref,is_original):
        target = __getCard_decoless(card_ref,is_original)
        if is_original:
            return target
        else:
            return self.decorateCard(target)

    def __getCard_decoless(self,card_ref,is_original):
        previous_cover.update(self.cover)
        previous_fill.update(self.fill)
        if ':' in card_ref:
            splits = card_ref.split(':',2)
            if splits[0] == self.name:
                card_ref = splits[1]
            else:
                return self.getCardFromLibMapping(splits[0],splits[1],is_original)
        return self.getCardFromCardMapping(card_ref,is_original)

    def getCardFromCardMapping(self,card_ref,is_original):
        if card_ref in self.cards.keys():
            return cards[card_ref].copy()
        elif card_ref in self.card_mapping:
            return self.card_mapping[card_ref].getCard(card_ref,is_original)
        else:
            # TODO EXPCEPTION CARD NOT FOUND
            pass

    def getCardFromLibMapping(self,lib_name,card_ref,is_original):
        if lib_name in self.libs_mapping.keys():
            return self.libs_mapping[lib_name].getCard(card_ref,is_original)
        else:
            # TODO EXCTPTION LIB NOT FOUND
            pass

    def add_sub_libraries(self,yamldata):
        def add_sub_library(self,yamldata):
            sublib = Library(yamldata)
            self.sub_libraries.update(sublib.name,sublib)
            # 将子库的卡片索引加入父库并映射到该子库
            for cardname in sublib.card_mapping.keys():
                self.card_mapping.update(cardname,sublib)
            # 将子库的所有卡片加入父库并映射到该子库
            for cardname in sublib.cards.keys():
                self.card_mapping.update(cardname,sublib)
            # 将子库的子库引加入父库并映射到该子库
            for libname in sublib.libs_mapping.keys():
                self.libs_mapping.update(libname,sublib)
            # 将该子库加入父库的子库索引
            self.libs_mapping.update(sublib.name,sublib)
        if yamldata is list:
            for data in yaml:
                add_sub_library(data)
        else:
            add_sub_library(data)
        # DEV NOTICE 如果映射的内存占用太大了就将每一个卡片和每一个子库的路径压成栈，交给根库来管理