import os
from typing import Optional
from pathlib import Path

dn = os.path.dirname

ENV_PATH = dn(dn(dn(__file__)))

def fmtpath(*paths) -> str:
    result = ''
    for path in paths:
        result += path.replace('/',os.sep)
    return result

def getbuilderpath(path:Optional[str] = None) -> Path:
    """获取构建器路径"""
    if not path:
        return Path(ENV_PATH)
    path = fmtpath(path)
    return Path(ENV_PATH) / path
