"""PCL 客户端信息"""
from typing import Optional, TYPE_CHECKING
from ..version import Version
from .branch import PCLBranch

if TYPE_CHECKING:
    from flask import Request

class PCLClient():
    """PCL 客户端信息"""
    def __init__(self):
        self.branch: PCLBranch
        self.version: Optional[Version]
        self.version_id: Optional[int]

    def is_pcl(self) -> bool:
        """是否为PCL2"""
        return self.branch.is_pcl()

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'branch': self.branch,
            'version': str(self.version)
        }

    def __hash__(self):
        return hash(str(self.branch)+str(self.version)+str(self.version_id))

    def above(self, other: 'PCLClient') -> bool:
        """判断当前版本是否大于其他版本"""
        if not self.version:
            raise ValueError("Current client version is None")
        if not self.is_pcl() or not other.is_pcl():
            return False
        return self.version > other.version

    def below(self, other: 'PCLClient') -> bool:
        """判断当前版本是否小于其他版本"""
        if not self.version:
            raise ValueError("Current client version is None")
        if not self.is_pcl() or not other.is_pcl():
            return False
        return self.version < other.version

    def __get_pcl_branch(self, web_request:'Request') -> PCLBranch:
        if pcl_branch := web_request.args.get('branch'):    # pcl_branch 参数优先
            return PCLBranch.from_string(pcl_branch, PCLBranch.NOT_PCL)
        if referer := web_request.headers.get('Referer', ''): # 其次通过 Referer 判断
            return PCLBranch.from_refer(referer)
        return PCLBranch.NOT_PCL

    def __get_pcl_version(self, web_request):
        if pcl_version := web_request.args.get('version'): # version 参数优先
            try:
                return Version.from_string(pcl_version)
            except Exception:
                return None
        uas = web_request.headers.get('User-Agent','') # 其次通过 User-Agent 判断
        uas = uas.split()
        if len(uas) >= 1:
            if pclver := uas[0].split('/'):
                if pclver[0] == 'PCL2':
                    return Version.from_string(pclver[1])
        return None

    @classmethod
    def from_request(cls, web_request) -> 'PCLClient':
        """从请求中获取PCL版本"""
        client = PCLClient()
        client.branch = client.__get_pcl_branch(web_request=web_request)
        client.version = client.__get_pcl_version(web_request=web_request)
        return client

DEFAULT_PCLCLIENT = PCLClient()
DEFAULT_PCLCLIENT.branch = PCLBranch.OFFICIAL
DEFAULT_PCLCLIENT.version = Version(2,9,0)