GIT_PULL = 'git pull -f'

class GithubAuthError(Exception):
    pass

def __update(request,project_path):
    if not vaild_from_github(request):
        raise GithubAuthError('Auth Failed')
    result = subprocess.check_output(GIT_PULL,cwd = project_path, shell=True)
    return result

def request_update(request,project_path):
    try:
        return (True,__update(request,project_path))
    except Exception as e:
        return (False,e.args)