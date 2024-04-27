esc_chars = {
    '&':'&amp;',
    '<':'&lt;',
	'>':'&gt;',
	'"':'&quot;',
	"'":'&apos;',
	'¡':'&iexcl;',
	'¢':'&cent;',
	'£':'&pound;',
	'¤':'&curren;',
	'¥':'&yen;',
	'¦':'&brvbar;',
	'§':'&sect;',
	'¨':'&uml;',
	'©':'&copy;',
	'ª':'&ordf;',
	'«':'&laquo;',
	'¬':'&not;',
	'®':'&reg;',
	'¯':'&macr;',
	'°':'&deg;',
	'±':'&plusmn;',
	'²':'&sup2;',
	'³':'&sup3;',
	'´':'&acute;',
	'µ':'&micro;',
	'¶':'&para;',
	'·':'&middot;',
	'¸':'&cedil;',
	'¹':'&sup1;',
	'º':'&ordm;',
	'»':'&raquo;',
	'¼':'&frac14;',
	'½':'&frac12;',
	'¾':'&frac34;',
	'¿':'&iquest;',
}

def decode_escape(string:str):
    '''反编码转义字符'''
    for key in esc_chars:
        string = string.replace(esc_chars[key],key)
    return string

def encode_escape(string:str):
    '''编码转义字符'''
    for key in esc_chars:
        string = string.replace(key,esc_chars[key])
    return string
