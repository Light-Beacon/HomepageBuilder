from homepagebuilder.interfaces import script,format_code, get_card_prop

@script('ForEach')
def for_each_script(store_name,iter_item_name,itemoutput,**kwargs):
    context = kwargs['context']
    card = kwargs['card']
    iter_item = get_card_prop(card=card,attr_name=iter_item_name)
    code = ''
    for item in iter_item:
        card_copy = card.copy()
        card_copy[store_name] = item
        code += format_code(itemoutput,data=card_copy,context=context,children_code='',err_output='false')
    return code