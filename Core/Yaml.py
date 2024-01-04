import yaml
import os

def ReadYaml(filepath):
    # 读取 YAML 文件
    if not os.path.exists(filepath):
        raise FileNotFoundError(f'{filepath} not exist!')
    with open(filepath,encoding='utf-8') as f:
        data = yaml.load(f,Loader=yaml.FullLoader)
        data.update('path',filepath)
        return data

def EnumDire(direpath,filename):
    # 遍历文件夹下所有文件夹(不递归打开), 读取其中名为 filename 的文件, 以 yaml 格式读取各个文件, 最后以列表形式输出
    output = []
    if not os.path.exists(direpath):
        raise FileNotFoundError(f'{direpath} not exist!')
    for dire in os.scandir(direpath):
        filepath = f'{dire}\\{filename}'
        if os.path.exists(filepath):
            output.append(ReadYaml(filepath))
    return output

def ScanDireReadYaml(direpath,regex):
    output = []
    if not os.path.exists(direpath):
        raise FileNotFoundError(f'{direpath} not exist!')
    for f in os.listdir(direpath):
        if re.match(regex,f):
            output.append((f,ReadYaml(f)))
    return output

def ScanDireRead(direpath,regex):
    # 返回所有目录下所有文件名符合正则表达式的文件，以元组（文件名，文件字符串）的列表输出
    output = []
    if not os.path.exists(direpath):
        raise FileNotFoundError(f'{direpath} not exist!')
    for f in os.listdir(direpath):
        if re.match(regex,f):
            with content = open(f'{direpath}\\{f}', "r+")
                output.append((f,str(content.read())))
    return output