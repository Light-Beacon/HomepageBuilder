from Core.project import Project

def script(card_name,proj:Project,**kwargs):
    return (card_name in proj.base_library.card_mapping.keys()) or (card_name in proj.base_library.cards.keys())
