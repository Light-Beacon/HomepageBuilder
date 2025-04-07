import yaml
from homepagebuilder.interfaces import script
from homepagebuilder.interfaces import file_reader
from homepagebuilder.core.types.context import Context

def genpath(list:list):
    """生成路径"""
    path = ""
    for i in list:
        if i == None:
            path += ".Child"
        else:
            path += f".Children[{i}]"
    return path

WINDOW_ROOT = "Content.Children[8].Child"
MODIFY_PATHS = {
"Title.LogoTitle": f"{WINDOW_ROOT}{genpath([1,3,0])}",
"Title.TextTitle": f"{WINDOW_ROOT}{genpath([1,3,1])}",
"Title.ImageTitle": f"{WINDOW_ROOT}{genpath([1,3,2])}",
"TopBar.Launch": f"{WINDOW_ROOT}{genpath([1,3,3,0])}",
"TopBar.Download": f"{WINDOW_ROOT}{genpath([1,3,3,1])}",
"TopBar.Link": f"{WINDOW_ROOT}{genpath([1,3,3,2])}",
"TopBar.Setup": f"{WINDOW_ROOT}{genpath([1,3,3,3])}",
"TopBar.Other": f"{WINDOW_ROOT}{genpath([1,3,3,4])}",
"Launch.Account.Microsoft.ChangeSkin.Button": f"{WINDOW_ROOT}{genpath([3,1,None,None,0,2,0,0,1,None,0])}",
"Launch.Account.Microsoft.AccountSettings.Button": f"{WINDOW_ROOT}{genpath([3,1,None,None,0,2,0,0,1,None,1])}",
"Launch.Account.Microsoft.SwitchAccount.Button": f"{WINDOW_ROOT}{genpath([3,1,None,None,0,2,0,0,1,None,2])}",
"Launch.Version.Switch": f"{WINDOW_ROOT}{genpath([3,1,None,None,0,0])}",
"Launch.Version.Modify": f"{WINDOW_ROOT}{genpath([3,1,None,None,0,1])}"
}

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
    for path, value in modifiers.items():
        for path_name, path_value in MODIFY_PATHS.items():
            path = path.replace(path_name, path_value)
        output += comp.toxaml({'PATH': path, 'VALUE': value}, context=context)
    return output