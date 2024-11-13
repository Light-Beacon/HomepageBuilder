from homepagebuilder.interfaces import config, script

@script('PublicConf')
def conf_script(key:str,default = None,**_kwargs):
    return config('Public.'+key,default)