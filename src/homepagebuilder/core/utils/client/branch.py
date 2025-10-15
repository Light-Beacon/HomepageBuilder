"""PCL2分支类型定义"""
from typing import Optional
from enum import Enum

class PCLBranch(Enum):
    """PCL2分支类型"""
    OFFICIAL = 1
    """官方版本PCL2"""
    OPEN_SOURCE = 10
    """开源版本PCL2"""
    COMMUNITY_EDITION = 11
    """社区版本PCL2"""
    NOT_PCL = 0
    """非PCL2"""

    class __Meta:
        ALIASES = {
            'official': 'OFFICIAL',
            'opensource': 'OPEN_SOURCE',
            'community': 'COMMUNITY_EDITION',
            'ce': 'COMMUNITY_EDITION',
            '': 'NOT_PCL',
        }

        Referers = {
            'ce.open.pcl2.server/': 'COMMUNITY_EDITION',
            'pcl2.open.server/': 'OPEN_SOURCE',
            'pcl2.server/': 'OFFICIAL',
        }

    def is_pcl(self) -> bool:
        """是否为PCL2"""
        return self.value != 0

    @classmethod
    def from_string(cls, name: 'Optional[str]',
                    default: 'Optional[PCLBranch]' = None) -> 'PCLBranch':
        """从字符串获取PCLBranch"""
        if name is None:
            return cls.NOT_PCL
        name = name.lower()
        branch_name = cls.__Meta.ALIASES.get(name)
        if branch_name and branch_name in cls:
            return cls[branch_name]
        else:
            return default or cls.NOT_PCL

    @classmethod
    def from_refer(cls, referer: str) -> 'PCLBranch':
        """从Referer获取PCLBranch"""
        for refer, branch_name in cls.__Meta.Referers.items():
            if referer.endswith(refer):
                return cls[branch_name]
        return cls.NOT_PCL
