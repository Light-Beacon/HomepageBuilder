from typing import TypedDict
from .builder import Builder
from .builder import Project

class BuildingEnvironment(TypedDict):
    """构建时环境"""
    builder: Builder
    project: Project
