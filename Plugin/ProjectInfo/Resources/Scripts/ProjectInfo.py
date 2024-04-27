import subprocess
def init(proj,**kwargs):
    res = proj.resources
    githash = get_githash(proj.base_path).removesuffix('\n')
    print(githash)
    res.data['global']['git.commit.hash'] = githash
    res.data['global']['git.commit.id'] = githash[:7]

def get_githash(path):
    githash = subprocess.check_output('git rev-parse HEAD',cwd = path, shell=True)
    return githash.decode("utf-8")