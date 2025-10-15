from typing import Tuple, List, Dict, Annotated, Optional, Union, Literal
from types import EllipsisType
from .client import PCLClient
from .branch import PCLBranch
from ..version import Version

MinVersionType = Annotated[Union[Version, EllipsisType],"min version"]
MaxVersionType = Annotated[Union[Version, EllipsisType],"max version"]

PCLBranchType = Annotated[Union[PCLBranch, Literal['*']],"PCL Branch or all branches"]
PCLVersionRange = Tuple[MinVersionType, MaxVersionType]
PCLVersionRanges = Annotated[Union[List[PCLVersionRange], Literal['*']],"PCL Version Range List or all versions"]


class PCLClientLimiter():
    def __init__(self, ruleset:Optional[Dict[PCLBranchType, PCLVersionRanges]] = None):
        self.ruleset:Dict[PCLBranchType, PCLVersionRanges] = ruleset or {}

    def add_rule(self, pcl_branch:PCLBranch,
                  versionrange:PCLVersionRange = (...,...)):
        minversion, maxversion = versionrange
        if isinstance(minversion, str):
            minversion = Version.from_string(minversion)
        if isinstance(maxversion, str):
            maxversion = Version.from_string(maxversion)
        if not self.ruleset.get(pcl_branch):
            self.ruleset[pcl_branch] = []
        self.ruleset[pcl_branch].append((minversion,maxversion)) # pyright: ignore[reportAttributeAccessIssue]


    def _check_accept(self, branch:Union[PCLBranch, Literal['*']],
                       version:Optional[Version]) -> bool:
        rules = self.ruleset.get(branch)
        if not rules:
            return False
        if branch == PCLBranch.NOT_PCL:
            return True
        if rules == '*':
            return True
        if not version:
            return False
        for rule in rules:
            if rule[0] <= version <= rule[1]:
                return True
        return False

    def check_accept(self, client:'PCLClient'):
        return self._check_accept('*', client.version) or self._check_accept(client.branch, client.version)
