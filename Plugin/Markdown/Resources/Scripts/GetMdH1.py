import markdown
import re
def script(card,args,res):
    exten = card['file_exten']
    if exten != 'md' and exten != 'markdown':
        return 'NOT A MARKDOWN DOCUMENT!'
    html = markdown.markdown(card['data'])
    titles = re.findall('<h1>(.*)</h1>',html)
    return titles[0]