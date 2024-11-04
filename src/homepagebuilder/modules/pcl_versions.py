from homepagebuilder.interfaces import script, format_code, Logger

logger = Logger('PCLVersionScript')

@script('IF_PCLNewerThan')
def newer_script(versionid,content,card,env,**_kwargs):
    vid = format_code('${client.versionid}',card,env=env)
    gtid = int(versionid)
    if not vid or not str.isalnum(vid):
        logger.warning('Cannot get version of pcl')
        return ''
    if int(vid) >= gtid:
        return content
    return ''

@script('IF_PCLOlderThan')
def lower_script(versionid,content,card,env,**_kwargs):
    vid = format_code('${client.versionid}',card,env=env)
    ltid = int(versionid)
    if not vid or not str.isalnum(vid):
        logger.warning('Cannot get version of pcl')
        return ''
    if int(vid) < ltid:
        return content
    return ''
