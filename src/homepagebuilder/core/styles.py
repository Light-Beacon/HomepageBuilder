'''
样式管理模块
'''

from typing import Dict

def get_style_code(context) -> str:
    '''获取样式代码'''
    styles:Dict[str,object] = context.styles
    xaml = ''
    for item in styles.values():
        if isinstance(item,str):
            xaml += item
        if isinstance(item,dict):
            for style in item['Styles']:
                xaml += f'<Style TargetType="{style["Target"]}" '
                if 'Key' in style:
                    xaml += f'x:Key="{style["Key"]}" '
                if 'BasedOn' in style:
                    xaml += f'BasedOn="{{StaticResource {style["BasedOn"]}}}"'
                xaml += '>\n'
                for setter_key in style['Setters']:
                    xaml += f'<Setter Property="{setter_key}" Value="{style["Setters"][setter_key]}"/>\n'
                xaml += '</Style>'
    return xaml
