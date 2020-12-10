import time
# from Crypto.Cipher import AES
import base64
import jwt
from ContestPlus.models import *
false = False
true = True

class Jwt:
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    salt = "asdfghjkl"

    def __init__(self, name):
        self.payload = {
            'name': name,
            'exp': int(time.time() + 86400)
        }

    def encode(self):
        token = jwt.encode(payload=self.payload, key=Jwt.salt, algorithm='HS256',
                           headers=Jwt.headers).decode('utf-8')
        return token


def user_type(request):
    try:
        user = User.objects.get(jwt=request.META.get('HTTP_JWT'))
    except User.DoesNotExist:
        return 'error', None
    return user.userType, user
