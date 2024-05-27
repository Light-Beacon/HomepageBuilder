def write_string(filepath:str,data:str):
    '''写入字符串文件'''
    with open(filepath, "w",encoding="utf-8") as file:
        return file.write(data)

write_func_mapping = {}

def write(file,*arg,func = None,**kwarg):
    '''写入文件'''
    if not func:
        if file.extention in write_func_mapping:
            func = write_func_mapping[file.extention]
        else:
            func = write_string
        return file.data
    return func(file.abs_path,*arg,**kwarg)

def regist_filewrite_function(func:callable,file_extens:str) -> None:
    '''注册写入后缀名为 `file_extens` 的文件的函数'''
    def reg_filewrite(func,file_exten:str):
        write_func_mapping[file_exten] = func
    if isinstance(file_extens,list):
        for exten in file_extens:
            reg_filewrite(func,exten)
    elif isinstance(file_extens,str):
        reg_filewrite(func,file_extens)
    else:
        raise TypeError()
