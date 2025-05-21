import yaml
from typing import Dict
from homepagebuilder.interfaces import script
from homepagebuilder.interfaces import file_reader
from homepagebuilder.core.types.context import Context
from homepagebuilder.core.utils.client import PCLClientLimiter, PCLEdition, PCLClient
from homepagebuilder.core.logger import Logger, is_debugging

logger = Logger('PCLMOD')

def genpath(list:list):
    """生成路径"""
    path = ""
    for i in list:
        if i is None:
            path += ".Child"
        else:
            path += f".Children[{i}]"
    return path

EDITION_MAPPING = {
    'offical': PCLEdition.OFFICAL,
    'opensource': PCLEdition.OPEN_SOURCE,
    'community': PCLEdition.COMMUNITY_EDITION,
}

class PCLStructure:
    """PCL 结构"""
    class PCLElementNode:
        def __init__(self, yaml_node:Dict):
            self.child = None
            self.children = {}
            self.yaml_node = yaml_node
            if isinstance(yaml_node,str): # 终端节点
                self.name = yaml_node
                self.is_endpoint = True
                logger.noisy('Created %s', self.name)
                return
            self.yaml_children = list(yaml_node.values())[0]
            if isinstance(self.yaml_children,list): # 集合容器
                self.is_collection_container = True
            elif isinstance(self.yaml_children,dict): # 单一元素容器
                self.is_collection_container = False
            else:
                raise TypeError(f"Invalid yaml node type: {type(self.yaml_children)}")
            if isinstance(yaml_node,dict):
                self.name = list(yaml_node.keys())[0]
                self.is_endpoint = False
                self.__build_tree()
            else:
                raise TypeError(f"Invalid yaml node type: {type(yaml_node)}")
            logger.noisy('Created %s', self.name)

        def __build_tree(self,):
            if self.is_endpoint:
                return
            if self.is_collection_container:
                index = 0
                for child in self.yaml_children:
                    node = PCLStructure.PCLElementNode(child)
                    self.children[node.name] = node, index
                    index += 1
            else:
                self.child = PCLStructure.PCLElementNode(self.yaml_children)

        def get_children(self, name):
            return self.children.get(name)
        
        def log_tree(self, deepth):
            logger.noisy('%s %s','  │' * deepth, self.name)
            if self.is_endpoint:
                return
            if self.is_collection_container:
                for child in self.children.values():
                    child[0].log_tree(deepth + 1)
            else:
                self.child.log_tree(deepth + 1)

    def __init__(self, yaml_data):
        self.yaml_data = yaml_data
        self.limiter = PCLClientLimiter()
        self.__init_limiter()
        self.root_node = self.PCLElementNode(self.yaml_data["content"])

    def __init_limiter(self):
        versions = self.yaml_data["versions"]
        for edition_str, version_range_str in versions.items():
            if edition := EDITION_MAPPING.get(edition_str):
                self.limiter.add_rule(edition, PCLStructure.__version_range_to_limiter_rule(version_range_str))
            else:
                raise ValueError('Unknown client edition %s', edition)

    def check(self, pcledition, version):
        return self.limiter.check_accept(pcledition, version)
            
    @classmethod
    def __version_range_to_limiter_rule(cls,range_list):
        min_ver = ... if range_list[0] == "..." else range_list[0]
        max_ver = ... if range_list[1] == "..." else range_list[1]
        return (min_ver, max_ver)

    def get_path(self, strpath:str):
        pclpath = []
        current_node = self.root_node
        splited_path = strpath.split('.')
        for node_str in splited_path:
            if not current_node:
                pclpath.append(node_str)
                continue
            if current_node.is_endpoint:
                current_node = None
                pclpath.append(node_str)
                continue
            if current_node.is_collection_container:
                if child_tuple := current_node.get_children(node_str):
                    child, index = child_tuple
                    pclpath.append(f"Children[{index}]")
                    current_node = child
                else:
                    current_node = None
                    pclpath.append(node_str)
            else:
                if node_str in ['', 'child']:
                    pclpath.append("Child")
                    current_node = current_node.child
                else:
                    current_node = None
                    pclpath.append(node_str)
        return '.'.join(pclpath)

    def log_tree(self):
        for edition, version in self.limiter.ruleset.items():
            logger.noisy('%s v%s:', edition, version)
        self.root_node.log_tree(0)
    
PCLStructure_LIST = []

def init(context:Context):
    global PCLStructure_LIST
    PCLStructure_LIST.append(PCLStructure(context.data['pcl_structure']))
    if is_debugging():
        for item in PCLStructure_LIST:
            item.log_tree()

def getpath(path, pcledition, version):
    global PCLStructure_LIST
    for pcl in PCLStructure_LIST:
        if pcl.check(pcledition, version):
            return pcl.get_path(path)
    raise ValueError(f"No Strcture can be used for PCL: {pcledition} v{version}")

@file_reader(['pclmodifier'])
def read_yaml(filepath:str) -> dict:
    ''' 读取 Yaml 文件 '''
    with open(filepath,encoding='utf-8') as f:
        card = {}
        card['modifiers'] = yaml.load(f,Loader=yaml.FullLoader)
        if not card['modifiers']:
            card['modifiers'] = {}
        card.update({'file_path':filepath})
        card['templates'] = ['PCLModifier']
        return card

@script('PCLModifierPresenter')
def modifier_presenter(card,context:Context,**_):
    modifiers = card['modifiers']
    output = ""
    comp = context.components['ModifierTextbox']
    client:PCLClient = context.client
    for path, value in modifiers.items():
        xamlpath = getpath(path, client.edition, client.version)
        output += comp.toxaml({'PATH': xamlpath, 'VALUE': value}, context=context)
    return output