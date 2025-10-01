"""
编码与反编码字符串模块
"""
import re

ESCAPE_CHARS = {
    '&':'&amp;',
    '<':'&lt;',
	'>':'&gt;',
	'"':'&quot;',
	"'":'&apos;'
}

SPECIAL_ESCAPE_CHARS = {
    '\t':'&#x0009;;',
    '\r':'&#x000D;',
	'\n':'&#x000A;',
}

UNESCAPED_BRACE_PATTEN = re.compile(r'^\s*\{(?!\}\s*\{)')
ESCAPED_BRACE_PATTEN = re.compile(r'\{\}')

def decode_escape(string:str):
    '''反编码转义字符'''
    for key,value in ESCAPE_CHARS.items():
        string = string.replace(value,key)
    for key,value in SPECIAL_ESCAPE_CHARS.items():
        string = string.replace(value,key)
    string = re.sub(ESCAPED_BRACE_PATTEN, '', string=string)
    return string

def encode_escape(string:str, with_special:bool = False, with_brace:bool = True):
    '''编码转义字符'''
    for key,value in ESCAPE_CHARS.items():
        string = string.replace(key,value)
    if with_special:
        for key,value in SPECIAL_ESCAPE_CHARS.items():
            string = string.replace(key,value)
    if with_brace:
        string = re.sub(UNESCAPED_BRACE_PATTEN, r'{}{', string=string)
    return string
