def script(**kwargs):
    card = kwargs['card']
    if 'data' in card:
        return card['data'] 
    else:
        return ''