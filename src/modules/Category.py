from core.types.project import Project
from interfaces import script

@script('Category')
def cats(cat_name,proj:Project,**kwargs):
    cards = list(filter(lambda card:isinstance(card.get('cats'),list)
           and cat_name in card.get('cats'), proj.get_all_card()))
    cardrefs = [card['card_id'] for card in cards]
    print(cardrefs)
    return str.join(';',cardrefs)
