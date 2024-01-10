from .FileIO import ScanDireReadYaml
class TemplateManager:
    def __init__(self,elements,scripts):
        self.templates = {}
        self.elements = elements
        self.scripts= scripts
        load_template('..\\Templates')
        # TODO

    def load_template(self,dir_path)
        for pair in ScanDireRead(dir_path)
            name = os.path.splitext(pair[0])[0]
            self.templates.update({name:pair[1]})

    def build(self,card):
        for template in card['templates']:
            if template not in self.templates.keys():
                continue
            if filter_match(templates[template],card):
                build_with_template(card,template)
                break
        else:
            # TODO NO TEMPLATE MATCHED EXCEPTION
            pass
        
    def build_with_template(self,card,template_name,child_code):
        if template_name = 'void'
            return child_str
        target_template = templates[template_name]
        code = ''
        for cpn in target_template['components']:
            if cpn in self.elements.keys():
                code += format_code(elements[cpn],card)
            elif cpn[0] == '$':
                if cpn[1:] in presenters.keys():
                    code += presenters[cpn[1:]].build(card)
                elif cpn.lower() == 'ChildPresenter':
                    code += child_code
                else:
                    pass # TODO presenter NOT FOUND
            else:
                pass # TODO ELEMENT NOT FOUND
        return self.build_with_template(card,target_template['base'],code)

    def filter_match(template,card):
        # 模版适用过滤器是否匹配
        pass # TODO