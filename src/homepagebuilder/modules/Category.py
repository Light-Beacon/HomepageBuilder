from homepagebuilder.interfaces import script

@script('Category')
def cats(cat_name, context, **kwargs):

    proj = context.project
    cards = list(filter(lambda card:isinstance(card.get('cats'),list)
        and cat_name in card.get('cats'), proj.get_all_card()))
    cardrefs = [card['card_id'] for card in cards]
    print(cardrefs)
    return str.join(';',cardrefs)
