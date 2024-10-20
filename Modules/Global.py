from Builder.Interfaces import script

@script('Global')
def global_vers(key,res,**kwarg):
    return res.data.get('global').get(key)