from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from yobaclub.models import User
from typing import Optional

class YobaBackend(BaseBackend):
    def authenticate(self, request=None, login: str=None, login_type: str=None, password: str=None) -> Optional[User]:
        try:
            if login_type == "mail":
                user = User.objects.get(mail=login)
            elif login_type == "login":
                user = User.objects.get(name=login)
        except User.DoesNotExist:
            return None
        hasher = PBKDF2PasswordHasher()
        if not hasher.verify(password, user.password):
            return None
        return user
    
    def get_user(self, user_id: int) -> Optional[User]:
        return User.objects.get(pk=user_id)