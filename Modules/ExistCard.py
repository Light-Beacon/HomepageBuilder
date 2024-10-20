from Builder.Core.types.project import Project
from Builder.Interfaces import script, format_code

@script('ExistCard')
def exist_card(card_name,env,card,**kwargs):
    card_name = format_code(card_name,data=card,env=env,children_code='',err_output='')
    return (card_name in env.get('project').base_library.card_mapping.keys()) \
        or (card_name in env.get('project').base_library.cards.keys())
