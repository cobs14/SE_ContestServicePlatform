import platform
import time
import random
import jwt
from ContestPlus.models import *
false = False
true = True


class Jwt:
    headers = {
        'alg': 'HS256',
        'typ': 'JWT'
    }
    salt = 'asdfghjkl'

    def __init__(self, name):
        self.payload = {'name': name, 'exp': int(time.time() + 86400)}

    def encode(self):
        token = jwt.encode(payload=self.payload, key=Jwt.salt,
                           algorithm='HS256', headers=Jwt.headers).decode('utf-8')
        return token


def user_type(request):
    try:
        user = User.objects.get(jwt=request.META.get('HTTP_JWT'))
    except User.DoesNotExist:
        return 'error', None
    return user.userType, user


def random_str(length):
    _str = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.choice(_str) for _ in range(length))


def update_group_code(user_id):
    user = User.objects.get(id=user_id)
    user.groupCode = random_str(12)
    user.save()
    return user.groupCode


def checkPlatform(string):
    print(platform.system())
    if platform.system() == "Linux":
        string.replace("\\", "/")
    return string
