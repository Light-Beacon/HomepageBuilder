"""
编码与反编码字符串模块
"""
esc_chars = {
    '&':'&amp;',
    '<':'&lt;',
	'>':'&gt;',
	'"':'&quot;',
	"'":'&apos;'
}

def decode_escape(string:str):
    '''反编码转义字符'''
    for key,value in esc_chars.items():
        string = string.replace(value,key)
    return string

def encode_escape(string:str):
    '''编码转义字符'''
    for key,value in esc_chars.items():
        string = string.replace(key,value)
    return string
