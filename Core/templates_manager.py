"""
模版管理器模块
"""
import traceback
from queue import Queue
from typing import List, Union
from .utils.formatter import format_code
from .ModuleManager import invoke_script
from .library import Library
from .logger import Logger
from .utils.event import trigger_invoke, trigger_return
from .utils import PropertySetter
from .types import BuildingEnvironment,TemplateManager as TemplateManagerBase

logger = Logger('Template')

def __is_filter_value_match(rule:str,value:str):
    if rule.startswith('$'):
        rule = rule[1:]
        if rule == 'HASVALUE' and value and len(value) > 0:
            return True
        if rule == 'EMPTY' and (value or len(value) == 0):
            return True
        return False
    else:
        if not value:
            return False
        rule = rule.lower()
        value = value.lower()
        return rule == value

def filter_match(template,card):
    '''检测卡片是否符合模版筛选规则'''
    if 'filter' not in template:
        return True
    if template['filter'] == 'never':
        return False
    for keyword in template['filter']:
        rules = template['filter'][keyword]
        if isinstance(rules,(str,int,bool,float)):
            if __is_filter_value_match(rule=str(rules),value = card.get(keyword)):
                return True
            else:
                return False
        if isinstance(rules,list):
            for rule in template['filter'][keyword]:
                if __is_filter_value_match(rule=str(rule),value = card.get(keyword)):
                    break # 所有匹配可能性有一个匹配就行
            else:
                return False
            continue
        raise TypeError()
    return True

class TemplateManager(TemplateManagerBase):
    '''模版管理器类'''
    def expend_card_placeholders(self,card:dict,children_code,env):
        '''展开卡片属性内所有占位符'''
        q = Queue()
        tries = 0
        for key in card:
            q.put(key)
        while not q.empty():
            if tries > q.qsize():
                logger.warning(f"检测到卡片中 {'、'.join(q.queue)} 属性无法被展开，跳过")
                break
            key = q.get()
            try:
                card[key] = format_code(card[key],card,env=env,children_code=children_code)
                tries = 0
            except KeyError:
                q.put(key)
                tries += 1
                continue
        return card

    def build_with_template(self,card,template_name,children_code,env:BuildingEnvironment) -> str:
        '''使用指定模版构建卡片'''
        if (not template_name) or template_name == 'void':
            return children_code
        target_template = env.get('templates')[template_name]
        code = ''
        card = PropertySetter(target_template.get('fill'),target_template.get('cover')).decorate(card)
        card = self.expend_card_placeholders(card,children_code,env)
        for cpn in target_template['components']:
            cpn = format_code(cpn,card,env,'')
            if cpn in env.get('components'):
                code += format_code(code = env.get('components')[cpn], card = card,
                                    env=env, children_code = children_code)
            elif cpn.startswith('$') or cpn.startswith('@'):
                args = cpn[1:].split('|')
                code += invoke_script(args[0],env=env,card=card,args=args[1:],children_code=children_code)
            else:
                logger.warning(f'{template_name}模版中调用了未载入的构件{cpn}，跳过')
        if 'containers' in target_template:
            tree_path = target_template['containers']
            code = self.packin_containers(tree_path,card,code,env)
        return self.build_with_template(card,target_template.get('base'),code,env)

    def packin_containers(self,tree_path:Union[str,List[str]],card,code:str,env:BuildingEnvironment):
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
                    if container in env.get('components'):
                        current_code = format_code(env.get('components')[container],
                                            card,env.get('project'),current_code)
                    else:
                        raise ValueError('容器路径中存在不存在的组件')
        return current_code

    @trigger_invoke('card.building')
    @trigger_return('card.builded')
    def build(self,card,env:BuildingEnvironment):
        '''构建卡片'''
        def try_build(self,card,template,env:BuildingEnvironment):
            try:
                return self.build_with_template(card,template,'',env)
            except Exception:
                logger.warning(f'构建卡片时出现错误：\n{traceback.format_exc()}Skipped.')
                return ''

        attr = card['templates']
        templates = env.get('templates')
        if isinstance(attr,str):
            template = templates[attr]
            if filter_match(template,card):
                return try_build(self,card,attr,env)
            else:
                logger.warning('卡片与其配置的模版要求不符，跳过')
                return ''
        elif isinstance(attr,list):
            for template_name in card['templates']:
                if template_name not in templates:
                    continue
                if filter_match(templates[template_name],card):
                    return try_build(self,card,template_name,env)
            logger.warning('卡片没有匹配的配置模版，跳过')
            return ''
        else:
            logger.warning('[TemplateManager] 模版列表类型无效，跳过')
