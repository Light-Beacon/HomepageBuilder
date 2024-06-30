from Interfaces import script

@script('RawPresenter')
def raw_presenter(card,**_):
    '''将卡片的 `data` 属性直接放入代码中'''
    if 'data' in card:
        return card['data']
    else:
        return ''

@script('ChildrenPresenter')
def children_presenter(children_code,**_):
    '''将子代码放入代码中'''
    return children_code
