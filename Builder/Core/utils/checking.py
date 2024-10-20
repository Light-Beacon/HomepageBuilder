"""类型检查限制模块"""

from Builder.Core.IO import File

def is_xaml(file:File) -> bool:
    "判断文件是否为Xaml"
    return file.extention == 'xaml'

def is_yaml(file:File) -> bool:
    "判断文件是否为Yaml"
    return file.extention in ['yml','yaml']
