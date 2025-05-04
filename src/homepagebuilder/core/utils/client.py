from enum import Enum
from typing import Union, Tuple, List, Dict, Annotated
from .checking import Version

class PCLEdition(Enum):
    """PCL2类型"""
    OFFICAL = 1
    """官方版本PCL2"""
    OPEN_SOURCE = 10
    """开源版本PCL2"""
    COMMUNITY_EDITION = 11
    """社区版本PCL2"""
    NOT_PCL = 0
    """非PCL2"""

    def is_pcl(self) -> bool:
        """是否为PCL2"""
        return self.value != 0

class PCLClientLimiter():
    def __init__(self):
        self.ruleset:Dict[PCLEdition, List[Tuple[Annotated[Version,"min version"], Annotated[Version,"max version"]]]] = {}

    def add_rule(self, pcledition, versionrange:Tuple[Union[Version|str], Union[Version|str]] = (...,...)):
        minversion, maxversion = versionrange
        if isinstance(minversion, str):
            minversion = Version.from_string(minversion)
        if isinstance(maxversion, str):
            maxversion = Version.from_string(maxversion)
        if not self.ruleset.get(pcledition):
            self.ruleset[pcledition] = []
        self.ruleset[pcledition].append((minversion,maxversion))

    def check_accept(self, pcledition, version):
        if isinstance(version, str):
            version = Version.from_string(version)
        rules = self.ruleset.get(pcledition)
        if not rules:
            return False
        for rule in rules:
            if version > rule[0] and version < rule[1]:
                break
        else:
            return False
        return True

class PCLClient():
    def __init__(self):
        self.edition: PCLEdition
        self.version: Version
        self.version_id: int

    def is_pcl(self) -> bool:
        """是否为PCL2"""
        return self.edition.is_pcl()

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'edition': self.edition,
            'version': str(self.version),
            'versionid': self.version_id
        }
        
    def __hash__(self):
        return hash(str(self.edition)+str(self.version)+str(self.version_id))

    def is_greater_than(self, other: 'PCLClient') -> bool:
        """判断当前版本是否大于其他版本"""
        if not self.is_pcl() or not other.is_pcl():
            return False
        return self.version > other.version

    def is_less_than(self, other: 'PCLClient') -> bool:
        """判断当前版本是否小于其他版本"""
        if not self.is_pcl() or not other.is_pcl():
            return False
        return self.version < other.version

    @classmethod
    def from_request(cls, web_request) -> 'PCLClient':
        """从请求中获取PCL版本"""
        client = PCLClient()
        client.edition = client.__getpcledition(web_request=web_request)
        client.version = client.__getpclver(web_request=web_request)
        client.version_id = client.__getpclverid(web_request=web_request)
        return client
    
    def __getpcledition(self, web_request) -> PCLEdition:
        refer = web_request.headers.get('Referer','')
        if refer.endswith('ce.open.pcl2.server/'):
            return PCLEdition.COMMUNITY_EDITION
        if refer.endswith('pcl2.open.server/'):
            return PCLEdition.OPEN_SOURCE
        if refer.endswith('pcl2.server/'):
            return PCLEdition.OFFICAL
        return PCLEdition.NOT_PCL

    def __getpclverid(self, web_request):
        refer = web_request.headers.get('Referer','')
        if not self.is_pcl():
            return None
        return int(refer[7:10])

    def __getpclver(self, web_request):
        uas = web_request.headers.get('User-Agent','')
        uas = uas.split()
        if len(uas) >= 1:
            if pclver := uas[0].split('/'):
                if pclver[0] == 'PCL2':
                    return pclver[1]
        return None

DEFAULT_PCLCLIENT = PCLClient()
DEFAULT_PCLCLIENT.edition = PCLEdition.OFFICAL
DEFAULT_PCLCLIENT.version = Version(2,99,99)
DEFAULT_PCLCLIENT.version_id = 9999