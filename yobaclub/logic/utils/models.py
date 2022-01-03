from django.db import models
from datetime import datetime


def get_current_timestamp():
    return datetime.utcnow().timestamp()

class User(models.Model):
    user_id = models.AutoField('User ID', primary_key=True, unique=True)
    name = models.CharField('User Name',unique=True, blank=False, max_length=25)
    mail = models.EmailField('User Email', unique=True, blank=False)
    password = models.CharField('User Passoword Hash', unique=False, blank=False, max_length=200)
    registered_time = models.FloatField('UTC Registration Date', unique=False, default=get_current_timestamp)
    is_admin = models.BooleanField('Is user an admin', unique=False, default=False)
    is_vip = models.BooleanField('Is user an VIP', unique=False, default=False)