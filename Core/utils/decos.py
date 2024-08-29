def enable_by(value,default_output=None):
    def enable_by_value_deco(func:callable):
        def wrapper(*args,**kwagrs):
            if value:
                return func(*args,**kwagrs)
            else:
                return default_output
        return wrapper
    return enable_by_value_deco