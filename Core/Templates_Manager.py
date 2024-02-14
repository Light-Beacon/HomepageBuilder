from .Code_Formatter import format_code
from .Resource import Resource
from .Code_Formatter import runScript
from queue import *

def filter_match(template,card):
    '''检测卡片是否符合模版筛选规则'''
    if 'filter' not in template:
        return True
    if template['filter'] is 'never':
        return False
    for keyword in template['filter']:
        for match in template['filter'][keyword]:
            if card[keyword] == match:
                break
        else:
            return False
    return True

class TemplateManager:
    def __init__(self,resources: Resource):
        self.resources = resources
        self.templates = resources.templates

    def expend_card_placeholders(self,card:dict,children_code):
        q = Queue()
        for key in card:
            q.put(key)
        while not q.empty():
            key = q.get()
            try:
                card[key] = format_code(str(card[key]),card,self.resources,children_code)
            except KeyError:
                q.put(key)
                continue
        return card
        
    def build_with_template(self,card,template_name,children_code) -> str:
        if template_name == None or template_name == 'void':
            return children_code
        target_template = self.templates[template_name]
        code = ''
        card = self.expend_card_placeholders(card,children_code)
        for cpn in target_template['components']:
            if cpn in self.resources.components:
                code += format_code(self.resources.components[cpn],card,self.resources,children_code)
            elif cpn[0] == '$':
                args = cpn[1:].split('|')
                code += runScript(args[0],self.resources,card,args,children_code)
            else:
                pass # TODO component NOT FOUND
        return self.build_with_template(card,target_template.get('base'),code)
    
    def build(self,card):
        for template in card['templates']:
            if template not in self.resources.templates:
                continue
            if filter_match(self.resources.templates[template],card):
                return self.build_with_template(card,template,'')
        else:
            # TODO NO TEMPLATE MATCHED EXCEPTION
            raise ValueError('NO TEMPLATE MATCHED EXCEPTION')
        