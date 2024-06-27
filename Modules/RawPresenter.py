from Interfaces import script

@script('RawPresenter')
def presenter(**kwargs):
    card = kwargs['card']
    if 'data' in card:
        return card['data']
    else:
        return ''
