import hmac
import subprocess
GIT_PULL = 'git pull -f'

class GithubAuthError(Exception):
    pass

def encrypt(secret,data):
    key = secret.encode('UTF-8')
    obj = hmac.new(key,msg=data,digestmod='sha1')
    return obj.hexdigest()

def vaild_from_github(request,secret):
    post_data = request.data
    token = encrypt(secret,post_data)
    sig = request.headers.get('X-Hub-Signature','').split('=')[-1]
    return sig == token
    
def __update(request,project_path,secret):
    if not vaild_from_github(request,secret):
        raise GithubAuthError('Auth Failed')
    result = subprocess.check_output(GIT_PULL,cwd = project_path, shell=True)
    return result

def request_update(request,project_path,secret):
    try:
        return (200,__update(request,project_path,secret))
    except Exception as e:
        return (401,str(e))