from homepagebuilder.core.utils.finder import find_using_resources
from homepagebuilder.core.formatter import format_code
from homepagebuilder.core.types import BuildingEnvironment
from homepagebuilder.interfaces import script

@script('RawPresenter')
def raw_presenter(card,env:BuildingEnvironment,**_):
    '''将卡片的 `data` 属性直接放入代码中'''
    data = card.get('data','')
    if 'usedresources' not in card:
        card['usedresources'] = find_using_resources(data)
    mark_used_resources(card['usedresources'],card,env)
    return data

@script('ChildrenPresenter')
def children_presenter(children_code,**_):
    '''将子代码放入代码中'''
    return children_code

def mark_used_resources(used_resources,card,env:'BuildingEnvironment'):
    for res_ref in used_resources:
        res_ref = format_code(code = res_ref,data=card,env=env)
        env.get('used_resources').add(res_ref)