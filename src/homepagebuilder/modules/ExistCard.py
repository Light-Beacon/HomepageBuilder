from homepagebuilder.interfaces import script, format_code

@script('ExistCard')
def exist_card(card_name,context,card,**kwargs):
    card_name = format_code(card_name,data=card,context=context,children_code='',err_output='')
    return (card_name in context.project.base_library.card_mapping.keys()) \
        or (card_name in context.project.base_library.cards.keys())
