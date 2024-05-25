import subprocess
from Core.debug import Logger
from Core.i18n import locale

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
