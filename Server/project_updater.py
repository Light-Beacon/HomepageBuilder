import hmac
import hashlib
import subprocess
import traceback
GIT_PULL = 'git pull -f'

class GithubAuthError(Exception):
    pass

def verify_signature(request,secret):
    body = request.data
    # https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries#python-example
    hash_object = hmac.new(secret.encode('utf-8'),
                           msg=body,digestmod=hashlib.sha1)
    expected_signature = "sha1=" + hash_object.hexdigest()
    signature_header = request.headers.get('X-Hub-Signature','')
    return hmac.compare_digest(expected_signature, signature_header)
    
def __update(request,project_dir,secret):
    if not verify_signature(request,secret):
        raise GithubAuthError('Auth Failed.')
    result = subprocess.check_output(GIT_PULL,cwd = project_dir, shell=True)
    return result

def request_update(request,project_dir,secret):
    try:
        return (200,__update(request,project_dir,secret))
    except GithubAuthError as e:
        return (401, str(e))
    except Exception as e:
        return (500, f"An Error occured while updating the project:\n {traceback.format_exc()}")