import subprocess
import datetime
from Core.logger import Logger
from Core.i18n import locale
from Interfaces.Events import on_card_building

logger = Logger('ProjectInfo')

def init(proj,**_):
    res = proj.resources
    githash = get_githash(proj.base_path).removesuffix('\n')
    logger.info(locale('projectinfo.gitversion',version=githash))
    res.data['global']['git.commit.hash'] = githash
    res.data['global']['git.commit.id'] = githash[:7]

def get_githash(path):
    githash = subprocess.check_output('git rev-parse HEAD',cwd = path, shell=True)
    return githash.decode("utf-8")

@on_card_building()
def get_card_last_update_time(_,card):
    if 'last_update' in card:
        return
    file = card.get('file')
    if not file:
        return
    timestamp = subprocess.check_output(r"git log -1 --format=%ct --follow -- " + file.abs_path ,cwd=file.direname, shell=True).decode("utf-8")
    dt = datetime.datetime.fromtimestamp(int(timestamp[:-1]))
    card['last_update'] = dt.date()
