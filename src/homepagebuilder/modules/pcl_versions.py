from homepagebuilder.interfaces import script, format_code, Logger

logger = Logger('PCLVersionScript')

@script('IF_PCLNewerThan')
def newer_script(versionid,content,card,context,**_kwargs):
    vid = format_code('${client.versionid}',card,context=context)
    if not vid:
        return
    gtid = int(versionid)
    if not vid or not str.isalnum(vid):
        logger.warning('Cannot get version of pcl')
        return ''
    if int(vid) >= gtid:
        return content
    return ''

@script('IF_PCLLowerThan')
def lower_script(versionid,content,card,context,**_kwargs):
    vid = format_code('${client.versionid}',card,context=context)
    if not vid:
        return
    ltid = int(versionid)
    if not vid or not str.isalnum(vid):
        logger.warning('Cannot get version of pcl')
        return ''
    if int(vid) < ltid:
        return content
    return ''
