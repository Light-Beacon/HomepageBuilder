from .Code_Formatter import format_code
from .Resource import Resource

def filter_match(template,card):
    # 检测卡片是否符合模版筛选规则
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

    def build_with_template(self,card,template_name,child_code):
        if template_name == 'void':
            return child_code
        target_template = self.templates[template_name]
        code = ''
        for cpn in target_template['components']:
            if cpn in self.resources.components:
                code += format_code(self.resources.components[cpn],card,self.resources)
            elif cpn[0] == '$':
                if cpn[1:] in self.resources.scripts:
                    code += self.resources.scripts[cpn[1:]].build(card)
                elif cpn.lower() == 'ChildPresenter':
                    code += child_code
                else:
                    pass # TODO script NOT FOUND
            else:
                pass # TODO component NOT FOUND
        return self.build_with_template(card,target_template['base'],code)
    
    def build(self,card):
        for template in card['templates']:
            if template not in self.resources.templates:
                continue
            if filter_match(self.resources.templates[template],card):
                self.build_with_template(card,template,'')
                break
        else:
            # TODO NO TEMPLATE MATCHED EXCEPTION
            pass
        