from .client import PCLClient, PCLClientLimiter, PCLEdition

FIXED_SWAPPED_TYPO_VERSIONS = PCLClientLimiter()
FIXED_SWAPPED_TYPO_VERSIONS.add_rule(PCLEdition.OFFICIAL, ('2.10.6',...))
FIXED_SWAPPED_TYPO_VERSIONS.add_rule(PCLEdition.OPEN_SOURCE, ('2.10.6',...))
#FIXED_SWAPPED_TYPO_VERSIONS.add_rule(PCLEdition.NOT_PCL, (...,...))

def replace_isswapped_typo(string:str, client:PCLClient):
    if FIXED_SWAPPED_TYPO_VERSIONS.check_accept(client):
        return string.replace('IsSwaped', 'IsSwapped')
    else:
        return string.replace('IsSwapped', 'IsSwaped')
