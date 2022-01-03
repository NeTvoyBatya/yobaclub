from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from datetime import datetime


def get_current_timestamp():
    return datetime.utcnow().timestamp()

class User(AbstractBaseUser):
    name = models.CharField('User Name',unique=True, blank=False, max_length=25)
    password = models.CharField('User Password Hash', unique=False, blank=False, max_length=2000)
    mail = models.EmailField('User Email', unique=True, blank=False)
    registered_time = models.FloatField('UTC Registration Date', unique=False, default=get_current_timestamp)
    is_admin = models.BooleanField('Is user an admin', unique=False, default=False)
    is_member = models.BooleanField('Is user an VIP', unique=False, default=False)
    is_active = models.BooleanField('Is user currently active', default=False)
    seen_news = models.BooleanField('Is user seen last news on main page', unique=False, default=False)
    last_login = models.DateTimeField(null=True, blank=True)

    user_id = models.AutoField('User ID', primary_key=True, unique=True)

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['password, mail']

    @property
    def isMember(self):
        return self.is_member

    @property
    def isAdmin(self):
        return self.is_admin
    
    def __str__(self) -> str:
        return f"User with name {self.name}"