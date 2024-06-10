from Core.project import Project
from Core.code_formatter import format_code

def script(card_name,proj:Project,card,**kwargs):
    card_name = format_code(card_name,card=card,project=proj,children_code='',err_output='')
    return (card_name in proj.base_library.card_mapping.keys()) \
        or (card_name in proj.base_library.cards.keys())
