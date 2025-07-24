"""
模版管理器模块
"""
import traceback
from queue import Queue
from typing import  TYPE_CHECKING
from .formatter import format_code, PropNotFormatedError
from .module_manager import invoke_script
from .logger import Logger
from .utils.event import set_triggers
from .utils.property import PropertySetter
from .config import is_debugging
from .i18n import locale as t

if TYPE_CHECKING:
    from typing import List, Union
    from .types import Context

SPECAIL_RULES = {
    'HASVALUE': lambda x: x and len(x) > 0,
    'EMPTY': lambda x: not x or len(x) == 0,
    'NEVER': lambda _: False,
}

def add_special_rule(name, func):
    '''添加特殊规则'''
    if name in SPECAIL_RULES:
        raise ValueError('Rule name already exists')
    SPECAIL_RULES[name] = func

logger = Logger('Template')

def __is_filter_value_match(rule,value):
    rule = str(rule)
    if rule.startswith('$'):
        rule = rule[1:]
        if rule_matcher := SPECAIL_RULES.get(rule):
            return rule_matcher(value)
        return False
    else:
        value = str(value)
        if not value:
            return False
        rule = rule.lower()
        value = value.lower()
        return rule == value

def filter_match(template,card):
    '''检测卡片是否符合模版筛选规则'''
    if not template:
        return False
    if 'filter' not in template:
        return True
    if template['filter'] == '$NEVER':
        return False
    for keyword in template['filter']:
        rules = template['filter'][keyword]
        if isinstance(rules,(str,int,bool,float)):
            if __is_filter_value_match(rule=rules,value = card.get(keyword)):
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

class TemplateManager():
    '''模版管理器类'''
    def expend_card_placeholders(self,card:dict,children_code,context):
        '''展开卡片属性内所有占位符'''
        q = Queue()
        tries = 0
        for key in card:
            q.put(key)
        while not q.empty():
            if tries > q.qsize():
                if is_debugging():
                    raise ValueError(f"检测到卡片中 {'、'.join(q.queue)} 属性无法被展开")
                else:
                    logger.warning("检测到卡片中 %s 属性无法被展开，跳过", '、'.join(q.queue))
                break
            key = q.get()
            try:
                card[key] = format_code(card[key],card,context=context,children_code=children_code)
                tries = 0
            except PropNotFormatedError:
                q.put(key)
                tries += 1
                continue
        return card

    def build_with_template(self,card,template_name,children_code,context:'Context') -> str:
        '''使用指定模版构建卡片'''
        logger.debug(t("template.build", template = template_name))
        if (not template_name) or template_name == 'void':
            return children_code
        target_template = context.templates[template_name]
        code = ''
        setter = PropertySetter(target_template.get('default'),target_template.get('override'))
        setter.default.update(card.get('fill',{}))  # 兼容性考虑
        setter.override.update(card.get('cover',{}))  # 兼容性考虑
        card = setter.decorate(card)
        card = self.expend_card_placeholders(card,children_code,context)
        for cpn in target_template['components']:
            cpn = format_code(cpn,card,context,'')
            if cpnobj := context.components.get(cpn):
                code += cpnobj.toxaml(card,context,children_code)
            elif cpn.startswith('$') or cpn.startswith('@'):
                args = cpn[1:].split('|')
                code += invoke_script(args[0],context=context,card=card,args=args[1:],children_code=children_code)
            elif not cpn == '':
                logger.warning(f'{template_name}模版中调用了未载入的构件{cpn}，跳过')
        if 'containers' in target_template:
            tree_path = target_template['containers']
            code = self.packin_containers(tree_path,card,code,context)
        return self.build_with_template(card,target_template.get('base'),code,context)

    def packin_containers(self,tree_path:'Union[str,List[str]]',card,code:str,context:'Context'):
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
        for container_name in containers:
            match container_name:
                case 'this':
                    current_code = code
                case 'base':
                    break
                case _:
                    if container_object := context.components.get(container_name):
                        current_code = container_object.toxaml(card,context,current_code)
                    else:
                        raise ValueError('容器路径中存在不存在的组件')
        return current_code

    @set_triggers('tm.buildcard')
    def build(self,card,context:'Context'):
        '''构建卡片'''
        def try_build(self,card,template,context:'Context'):
            try:
                return self.build_with_template(card,template,'',context)
            except Exception as ex:
                if is_debugging():
                    raise ex
                else:
                    logger.warning('构建卡片时出现错误：\n%sSkipped.', traceback.format_exc())
                    return ''

        attr = card['templates']
        templates = context.templates
        if isinstance(attr,str):
            template = templates[attr]
            if filter_match(template,card):
                return try_build(self,card,attr,context)
            else:
                logger.warning('卡片与其配置的模版要求不符，跳过')
                return ''
        elif isinstance(attr,list):
            for template_name in card['templates']:
                if filter_match(templates.get(template_name),card):
                    return try_build(self,card,template_name,context)
            if is_debugging():
                raise ValueError('卡片没有匹配的配置模版')
            else:
                logger.warning('卡片没有匹配的配置模版，跳过')
            return ''
        else:
            logger.warning('[TemplateManager] 模版列表类型无效，跳过')
