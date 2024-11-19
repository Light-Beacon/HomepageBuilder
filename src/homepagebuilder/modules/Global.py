from homepagebuilder.interfaces import script

@script('Global')
def global_vers(key,context,**kwarg):
    return context.data.get(key)