import re

def format_code(code,card,scripts):
    pattern = r'\{\$([^}]+)\}'
    matches = re.findall(pattern, text)
    for match in matches:
        qurey_tuple = match.split('|')
        attr_name = qurey_tuple[0]
        if attr_name = 'script':
            replacement = qurey_tuple[[1]](qurey_tuple[2:])
        elif attr_name in card.keys():
            replacement = card[attr_name]
        else:
            continue
        code = re.sub(rf'\{{\${match}\}}', replacement, code)
    return code