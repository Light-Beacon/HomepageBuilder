import yaml
import os
import re

def readString(filepath:str):
    # 读取字符串文件
    with open(filepath, "r+") as file:
        return file.read()
    
def readYaml(filepath):
    # 读取 YAML 文件
    if not os.path.exists(filepath):
        raise FileNotFoundError(f'{filepath} not exist!')
    with open(filepath,encoding='utf-8') as f:
        data = yaml.load(f,Loader=yaml.FullLoader)
        data.update('path',filepath)
        return data
    
read_func_mapping = {
    'yml':readYaml,
}

def ScanDire(direpath:str, regex:str, asraw:bool = False):
    # 返回所有目录下所有文件名符合正则表达式的文件，以元组（读取出的信息，文件名，文件名后缀）的列表输出
    output = []
    if not os.path.exists(direpath):
        raise FileNotFoundError(f'{direpath} not exist!')
    for f in os.listdir(direpath):
        if re.match(regex,f):
            filename, exten = os.path.splitext(f)
            f = f'{direpath}\\{f}'
            exten = exten[1:]
            try:
                if asraw or exten not in read_func_mapping:
                    output.append((readString(f),filename,exten))
                else:
                    output.append((read_func_mapping[exten](f),filename,exten))
            except:
                print(f'Fail to load {f}')            
    return output

def ScanSubDire(direpath:str, regex:str, asraw:bool = False):
    # 遍历文件夹下所有文件夹(不递归打开), 读取其中符合正则表达式的文件, 以 yaml 格式读取各个文件, 最后以元组（读取出的信息，文件名，文件名后缀）的列表形式输出
    output = []
    if not os.path.exists(direpath):
        raise FileNotFoundError(f'{direpath} not exist!')
    for dire in os.scandir(direpath):
        output.append(ScanDire(dire,regex,asraw))
    return output