from homepagebuilder.interfaces import config, script

@script('public_conf')
def conf_script(key:str,default = None,**_kwargs):
    return config('Public.'+key,default)