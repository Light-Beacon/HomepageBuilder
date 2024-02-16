from typing import Dict,Union
def getStyleCode(styles:Dict[str,object]) -> str:
    xaml = ''
    for item in styles.values():
        if type(item) is str:
            xaml += item
        if type(item) is dict:
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