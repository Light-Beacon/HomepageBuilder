def LogInfo(infomation:str):
    print(f'{blue}[INFO]{clear}{infomation}')

def LogWarning(infomation:str):
    print(f'{yellow}[WARNING]{clear}{infomation}')

def LogDebug(infomation:str):
    print(f'{green}[DEBUG]{clear}{infomation}')
    
def LogError(infomation:str):
    print(f'{red}[ERROR]{infomation}')
    return infomation


clear = '\033[0m'  
red = '\033[31m'
green = '\033[32m'
yellow = '\033[33m'
blue = '\033[34m'