from Core.Project import Project

def script(cat_name,proj:Project,**kwargs):
    cards = list(filter(lambda card:isinstance(card.get('cats'),list)
           and cat_name in card.get('cats'), proj.getAllCard()))
    cardrefs = [card['card_id'] for card in cards]
    print(cardrefs)
    return str.join(';',cardrefs)