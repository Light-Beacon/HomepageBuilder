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
        add_sub_libraries(self,EnumDire(self.location,'library.yaml'))  # 遍历添加子库

    def add_sub_libraries(self,yamldata):
        def add_sub_library(self,yamldata):
            sublib = Library(yamldata)
            self.sub_libraries.update(sublib.name,sublib)
            # 将子库的卡片索引加入父库并映射到该子库
            for cardname in sublib.card_mapping.keys():
                self.card_mapping.update(cardname,sublib.name)
            # 将子库的所有卡片加入父库并映射到该子库
            for cardname in sublib.cards.keys():
                self.card_mapping.update(cardname,sublib.name)
            # 将子库的子库引加入父库并映射到该子库
            for libname in sublib.libs_mapping.keys():
                self.libs_mapping.update(libname,sublib.name)
            # 将该子库加入父库的子库索引
            self.libs_mapping.update(sublib.name,sublib.name)
        is yamldata is list:
            for data in yaml:
                add_sub_library(data)
        else:
            add_sub_library(data)
        # DEV NOTICE 如果映射的内存占用太大了就将每一个卡片和每一个子库的路径压成栈，交给根库来管理