from homepagebuilder.interfaces import script

@script('Global')
def global_vers(key,env,**kwarg):
    return env['data'].get(key)