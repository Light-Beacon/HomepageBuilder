import yaml
from homepagebuilder.interfaces import script
from homepagebuilder.interfaces import file_reader
from homepagebuilder.core.types.context import Context
from homepagebuilder.core.utils.client import PCLClientLimiter, PCLEdition, PCLClient

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
        def __init__(self, yaml_node):
            self.child = None
            self.children = {}
            self.yaml_node = yaml_node
            if isinstance(yaml_node,str):
                self.name = yaml_node
                self.is_endpoint = True
                return
            self.yaml_children = yaml_node.items()[0]
            if isinstance(self.yaml_children,list):
                self.is_collection_container = True
            elif isinstance(self.yaml_children,dict):
                self.is_collection_container = False
            else:
                raise TypeError(f"Invalid yaml node type: {type(self.yaml_children)}")
            if isinstance(yaml_node,dict):
                self.name = yaml_node.keys()[0]
                self.is_endpoint = False
                self.__build_tree()
            else:
                raise TypeError(f"Invalid yaml node type: {type(yaml_node)}")

        def __build_tree(self,):
            if self.is_endpoint:
                return
            if self.is_collection_container:
                self.child = PCLStructure.PCLElementNode(self.yaml_children)
            for child_yaml_node in self.yaml_children:
                child_node = PCLStructure.PCLElementNode(child_yaml_node)
                name = child_node.name
                self.children[name] = child_node

        def get_children(self, name):
            return self.children.get(name)

    def __init__(self, yaml_data):
        self.yaml_data = yaml_data
        self.limiter = PCLClientLimiter()
        self.__init_limiter()
        self.root_node = self.PCLElementNode(self.yaml_data["content"])

    def __init_limiter(self):
        versions = self.yaml_data["versions"]
        for edition, key in EDITION_MAPPING.items():
            if offical_version_range := versions.get(key):
                self.limiter.add_rule(edition, PCLStructure.__version_range_to_limiter_rule(offical_version_range))

    def check(self, pcledition, version):
        return self.limiter.check_accept(pcledition, version)
            
    @classmethod
    def __version_range_to_limiter_rule(cls,range_list):
        min_ver = ... if range_list[0] == "..." else range_list[0]
        max_ver = ... if range_list[0] == "..." else range_list[0]
        return (min_ver, max_ver)

    def get_path(self, strpath:str):
        pclpath = ""
        current_node = self.root_node
        while True:
            name, new_strpath = strpath.split('.', 1)
            if current_node.is_endpoint:
                break
            if current_node.is_collection_container:
                if name in ['', 'child']:
                    pclpath += "Child."
                    current_node = current_node.child
                else:
                    break
            else:
                if child_tuple := current_node.get_children(name):
                    index, child = child_tuple
                    pclpath += f"Children[{index}]."
                    current_node = child
                else:
                    break
            strpath = new_strpath
        pclpath += strpath
        return pclpath

PCLStructure_LIST = []

def init(context:Context):
    global PCLStructure_LIST
    PCLStructure_LIST.append(PCLStructure(context.data['pcl_structure']))

def getpath(path, pcledition, version):
    global PCLStructure_LIST
    for pcl in PCLStructure_LIST:
        if pcl.check(pcledition, version):
            return pcl.get_path(path)
    raise ValueError(f"Path {path} not found in PCLStructure")

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
    client:PCLClient = context.setter.get('client')
    for path, value in modifiers.items():
        xamlpath = getpath(path, client.edition, client.version)
        output += comp.toxaml({'PATH': xamlpath, 'VALUE': value}, context=context)
    return output