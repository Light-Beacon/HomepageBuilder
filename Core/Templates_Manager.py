from .Code_Formatter import format_code
from .Resource import Resource
from .scriptRunner import runScript

def filter_match(template,card):
    '''检测卡片是否符合模版筛选规则'''
    if 'filter' not in template:
        return True
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

    def build_with_template(self,card,template_name,child_code) -> str:
        if template_name == None or template_name == 'void':
            return child_code
        target_template = self.templates[template_name]
        code = ''
        for cpn in target_template['components']:
            if cpn in self.resources.components:
                code += format_code(self.resources.components[cpn],card,self.resources)
            elif cpn[0] == '$':
                args = cpn[1:].split('|')
                if args[0] in self.resources.scripts:
                    code += runScript(self.resources.scripts[args[0]],card,args)
                elif cpn.lower() == 'ChildrenPresenter':
                    code += child_code
                else:
                    pass # TODO script NOT FOUND
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
        