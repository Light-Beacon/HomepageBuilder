import subprocess
import datetime
import os
from core.logger import Logger
from core.i18n import locale
from interfaces.Events import on_card_building, on_project_loaded
from interfaces import enable_by_config, config as sys_config, enable_by

def gitinfo_config(key):
    return sys_config('ProjectInfo.GitInfo.' + key)

logger = Logger('ProjectInfo')


def is_git_installed() -> bool:
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception:
        return False
    
def check_git_installtion() -> bool:
    if not gitinfo_config('Enable'):
        return False
    is_installed = is_git_installed()
    if not is_installed and not gitinfo_config('NoProduceNotInstalledWarning'):
        logger.warning(locale('projectinfo.git.notinstalled'))
        logger.warning(locale('projectinfo.git.disablehint', hide_config_key = 'NoProduceNotInstalledWarning'))
    return is_installed

IS_GIT_INSTALLED = check_git_installtion()

def is_git_repo(directory):
    return os.path.exists(os.path.join(directory, '.git'))

@on_project_loaded()
@enable_by_config('ProjectInfo.GitInfo.Enable')
@enable_by(IS_GIT_INSTALLED)
def set_githash(proj,*_,**__):
    res = proj.resources
    res.data['global']['git.isrepo'] = is_git_repo(proj.base_path)
    if not res.data['global']['git.isrepo']:
        if not gitinfo_config('NoProduceNotRepoWarning'):
            logger.warning(locale('projectinfo.git.isnotrepo'))
            logger.warning(locale('projectinfo.git.disablehint', hide_config_key = 'NoProduceNotRepoWarning'))
        return
    githash = get_githash(proj.base_path).removesuffix('\n')
    logger.info(locale('projectinfo.git.version',version=githash))
    res.data['global']['git.commit.hash'] = githash
    res.data['global']['git.commit.id'] = githash[:7]

def get_githash(path):
    githash = subprocess.check_output('git rev-parse HEAD',cwd = path, shell=True)
    return githash.decode("utf-8")

@on_card_building()
@enable_by_config('ProjectInfo.GitInfo.Enable')
@enable_by(IS_GIT_INSTALLED)
def get_card_last_update_time(_tm,card,env,*args,**kwargs):
    res = env.get('resource')
    if not res.data['global']['git.isrepo']:
        return
    if 'last_update' in card:
        return
    file = card.get('file')
    if not file:
        return
    timestamp = subprocess.check_output(r"git log -1 --format=%ct --follow -- " + file.abs_path ,cwd=file.direname, shell=True).decode("utf-8")
    if len(timestamp) == 0:
        return
    dt = datetime.datetime.fromtimestamp(int(timestamp[:-1]))
    card['last_update'] = dt.date()
