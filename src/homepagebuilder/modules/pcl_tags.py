from homepagebuilder.core.utils.client import PCLClientLimiter, PCLBranch, DEFAULT_PCLCLIENT
from homepagebuilder.core.utils.version import Version
from homepagebuilder.core.types import Context
from homepagebuilder.interfaces import script

TAGS = {
    '#页面:联机': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,4,0), Version(2,5,1))],
        PCLBranch.COMMUNITY_EDITION: [(Version(2,12,10), ...)]}),
    '#事件:内存优化': PCLClientLimiter({
        '*': [(Version(2,6,2), ...)]}),
    '#事件:切换页面': PCLClientLimiter({
        '*': [(Version(2,6,4), ...)]}),
    '#事件:安装整合包': PCLClientLimiter({
        '*': [(Version(2,6,4), ...)]}),
    '#事件:打开网页:minecraft': PCLClientLimiter({
        '*': [(Version(2,6,4), ...)]}),
    '#控件:MyIconTextButton': PCLClientLimiter({
        '*': [(Version(2,6,4), ...)]}),
    '#替换标记:hint': PCLClientLimiter({
        '*': [(Version(2,6,5), ...)]}),
    '#替换标记:cave': PCLClientLimiter({
        '*': [(Version(2,6,5), ...)]}),
    '#控件:MyIconButton:支持事件': PCLClientLimiter({
        '*': [(Version(2,6,5), ...)]}),
    '#控件:MyListItem:设置联网帮助': PCLClientLimiter({
        '*': [(Version(2,7,4), ...)]}),
    '#控件:MyImage': PCLClientLimiter({
        '*': [(Version(2,8,9), ...)]}),
    '#控件:MyTextBox:支持CornerRadius': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,9,2), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,9,2), ...)],
        PCLBranch.COMMUNITY_EDITION: [(Version(2,10,5), ...)]}),
    '#控件:MyCard:支持CornerRadius': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,9,2), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,9,2), ...)],
        PCLBranch.COMMUNITY_EDITION: [(Version(2,10,5), ...)]}),
    '#控件:MyCard:支持Inline': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,9,2), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,9,2), ...)],
        PCLBranch.COMMUNITY_EDITION: [(Version(2,10,5), ...)]}),
    '#控件:WebBrowser:禁用': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,9,3), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,9,3), ...)],
        PCLBranch.COMMUNITY_EDITION: [(Version(2,11,1), ...)]}),
    '#系统:限制命名空间引用': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,9,3), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,9,3), ...)],
        PCLBranch.COMMUNITY_EDITION: [(Version(2,11,1), ...)]}),
    '#控件:MyHint:支持Theme': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,1), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,1), ...)],
        PCLBranch.COMMUNITY_EDITION: [(Version(2,11,2), ...)]}),
    '#控件:MyHint:支持HasBorder': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,1), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,1), ...)],
        PCLBranch.COMMUNITY_EDITION: [(Version(2,11,2), ...)]}),
    '#控件:MyDropShadow': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,1), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,1), ...)],
        PCLBranch.COMMUNITY_EDITION: [(Version(2,11,2), ...)]}),
    '#控件:MyDropShadow:ShadowRadius': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,1), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,1), ...)],
        PCLBranch.COMMUNITY_EDITION: [(Version(2,11,2), ...)]}),
    '#事件:修改设置': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,6), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,6), ...)]}),
    '#替换标记:varible': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,9), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,9), ...)]}),
    '#替换标记:setup': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,9), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,9), ...)]}),
    '#替换标记:pcl_version': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,9), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,9), ...)]}),
    '#替换标记:pcl_version_code': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,9), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,9), ...)]}),
    '#替换标记:pcl_version_branch': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,9), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,9), ...)]}),
    '#替换标记:pcl_branch': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,9), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,9), ...)]}),
    '#替换标记:identify': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,9), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,9), ...)]}),
    '#替换标记:path_with_name': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,9), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,9), ...)]}),
    '#替换标记:path_temp': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,9), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,9), ...)]}),
    '#系统:替换标记支持主页地址': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,9), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,9), ...)]}),
    '#控件:MyCard:支持事件': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,9), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,9), ...)]}),
    '#控件:MyCheckBox:支持事件': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,9), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,9), ...)]}),
    '#控件:MyRadioBox:支持事件': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,9), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,9), ...)]}),
    '#控件:MyRadioButton:支持事件': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,9), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,9), ...)]}),
    '#控件:MyComboBox:支持事件': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,9), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,9), ...)]}),
    '#控件:MyExtraButton:支持事件': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,9), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,9), ...)]}),
    '#控件:MyExtraTextButton:支持事件': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,9), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,9), ...)]}),
    '#控件:MyMenuItem:支持事件': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,9), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,9), ...)]}),
    '#控件:MyTextBox:支持事件': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,9), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,9), ...)]}),
    '#控件:MySearchBox:支持事件': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,9), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,9), ...)]}),
    '#系统:CustomEventService': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,10,9), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,10,9), ...)]}),
    '#控件:MyImage:FallbackSource:支持网络图片': PCLClientLimiter({
        PCLBranch.OFFICIAL: [(Version(2,8,9), Version(2,10,6)), (Version(2,10,9), ...)],
        PCLBranch.OPEN_SOURCE: [(Version(2,8,9), Version(2,10,6)), (Version(2,10,9), ...)]}),
    # CE 专用标签
    '#系统:支持深色模式': PCLClientLimiter({
        PCLBranch.COMMUNITY_EDITION: [(Version(2,10,0), ...)]}),
}

@script('IF_PCLSupport')
def if_pclsupport(tag:str, content):
    """判断当前客户端是否支持某个功能"""
    client = Context.get_current_context().client or DEFAULT_PCLCLIENT
    if tag_limiter := TAGS.get(tag):
        if tag_limiter.check_accept(client):
            return content
    return ''
