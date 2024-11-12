'''
工程更新模块
'''
import hmac
import hashlib
import subprocess
import traceback
from ..core.logger import Logger

GIT_PULL = 'git pull -f'

logger = Logger('ProjectUpdater')

class GitHubAuthError(Exception):
    '''GitHub 验证错误'''

def verify_signature(request,secret):
    '''验证GH签名'''
    body = request.data
    # https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries#python-example
    hash_object = hmac.new(secret.encode('utf-8'),
                           msg=body,digestmod=hashlib.sha1)
    expected_signature = "sha1=" + hash_object.hexdigest()
    signature_header = request.headers.get('X-Hub-Signature','')
    return hmac.compare_digest(expected_signature, signature_header)

def __update(request,project_dir,secret):
    if not verify_signature(request,secret):
        raise GitHubAuthError('Auth Failed.')
    result = subprocess.check_output(GIT_PULL,cwd = project_dir, shell=True)
    return result

def request_update(request,project_dir,secret):
    '''请求更新'''
    try:
        return (200,__update(request,project_dir,secret))
    except GitHubAuthError:
        return (401, "Auth Failed.")
    except Exception as e:
        logger.error("An Error occured while updating the project: %s\n %s",e,traceback.format_exc())
        return (500, "An Error occured while updating the project")
