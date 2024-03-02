from .Code_Formatter import format_code
from .Resource import Resource
from .Code_Formatter import runScript
from .Debug import LogWarning
from .Library import Library
from typing import List, Union
from queue import *
import traceback

def __is_filter_value_match(rule:str,value:str):
    if rule.startswith('$'):
        rule = rule[1:]
        if rule == 'HASVALUE' and value != None and len(value) > 0:
            return True
        if rule == 'EMPTY' and (value == None or len(value) == 0):
            return True
        return False
    else:
        return rule == value

def filter_match(template,card):
    '''检测卡片是否符合模版筛选规则'''
    if 'filter' not in template:
        return True
    if template['filter'] == 'never':
        return False
    for keyword in template['filter']:
        rules = template['filter'][keyword]
        if isinstance(rules,str):
            if not __is_filter_value_match(rule=rules,value = card.get(keyword)):
                return False
        if isinstance(rules,list):
            for rule in template['filter'][keyword]:
                if __is_filter_value_match(rule=rule,value = card.get(keyword)):
                    break
            else:
                return False
            continue
        raise TypeError()
    return True

class TemplateManager:
    def __init__(self,resources: Resource):
        self.resources = resources
        self.templates = resources.templates

    def expend_card_placeholders(self,card:dict,children_code):
        q = Queue()
        tries = 0
        for key in card:
            q.put(key)
        while not q.empty():
            if tries > q.qsize():
                LogWarning(f"[TemplateManager] 检测到卡片中 {'、'.join(q.queue)} 属性无法被展开，跳过")
                break
            key = q.get()
            try:
                card[key] = format_code(str(card[key]),card,self.resources,children_code)
                tries = 0
            except KeyError:
                q.put(key)
                tries += 1
                continue
        return card
        
    def build_with_template(self,card,template_name,children_code) -> str:
        if template_name == None or template_name == 'void':
            return children_code
        target_template = self.templates[template_name]
        card = Library.decorateCard(card,target_template.get('fill'),
                                    target_template.get('cover'))
        code = ''
        card = self.expend_card_placeholders(card,children_code)
        for cpn in target_template['components']:
            if cpn in self.resources.components:
                code += format_code(code = self.resources.components[cpn],card = card,
                                    resources=self.resources,children_code = children_code)
            elif cpn.startswith('$') or cpn.startswith('@'):
                args = cpn[1:].split('|')
                code += runScript(args[0],self.resources,card,args,children_code)
            else:
                pass # TODO component NOT FOUND
        if 'containers' in target_template:
            tree_path = target_template['containers']
            code = self.packin_containers(tree_path,card,code)
        return self.build_with_template(card,target_template.get('base'),code)
    
    def packin_containers(self,tree_path:Union[str,List[str]],card,code:str):
        '''按照容器组件路径包装'''
        containers:list = []
        if isinstance(tree_path,str):
            containers = tree_path.replace(' ','').split('->')
        elif isinstance(tree_path,list):
            containers = tree_path
        else:
            raise TypeError('容器路径类型无效')
        containers.reverse()
        current_code = code
        for container in containers:
            match container:
                case 'this':
                    current_code = code
                case 'base':
                    break
                case _:
                    if container in self.resources.components:
                        current_code = format_code(self.resources.components[container],
                                            card,self.resources,current_code)
                    else:
                        raise ValueError('容器路径中存在不存在的组件')
        return current_code
                        
    def build(self,card):
        def try_build(self,card,template):
            try:
                return self.build_with_template(card,template,'')
            except Exception as e:
                LogWarning(f'[TemplateManager] 构建卡片时出现错误：\n{traceback.format_exc()}Skipped.')
                return ''
        
        attr = card['templates']
        if isinstance(attr,str):
            template = self.resources.templates[attr]
            if filter_match(template,card):
                return try_build(self,card,attr)
            else:
                LogWarning('[TemplateManager] 卡片与其配置的模版要求不符，跳过')
                return ''
        elif isinstance(attr,list):
            for template_name in card['templates']:
                if template_name not in self.resources.templates:
                    continue
                if filter_match(self.resources.templates[template_name],card):
                   return try_build(self,card,template_name)
            else:
                LogWarning('[TemplateManager] 卡片没有匹配的配置模版，跳过')
                return ''
        else:
            LogWarning('[TemplateManager] 模版列表类型无效，跳过')

        