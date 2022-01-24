from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from datetime import datetime
import secrets
from json import loads, dumps


def create_hex():
    return secrets.token_hex(10)

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

class Thing(models.Model):
    title = models.CharField('Name of the thing',unique=True, blank=False, max_length=40)
    description = models.TextField('Description of the thing', unique=False, blank=False)
    files_links = models.TextField('List of the thing\'s files with separators', blank=True)
    author = models.CharField('Name of the thing\'s author', unique=False, blank=False, default="Аноним", max_length=25)
    thing_id = models.AutoField('INT ID of the thing', primary_key=True, unique=True)

class CinemaRoom(models.Model):
    name = models.CharField("Name of the room", unique=True, blank=False, max_length=25)
    login_only = models.BooleanField("Only members can join the room", unique=False)
    users_in = models.TextField("Users currently in room", default="[]")
    messages = models.TextField("Messages in this room's chat", default="[]")
    admin = models.CharField("Room admin's channel name", null=True, max_length=100)
    room_id = models.CharField("HEX-ID of the room", unique=True, max_length=15, default=create_hex, primary_key=True)
    waiting_users = models.TextField("New users, waiting for state", default="[]")

    def add_message(self, message):
        messages = loads(self.messages)
        messages.append(message.__dict__())
        self.messages = dumps(messages)
        self.save()
    
    def new_user(self, user):
        users = loads(self.users_in)
        users.append(user.__dict__())
        self.users_in = dumps(users)
        self.save()

    def remove_user(self, channel_name: str):
        users = loads(self.users_in)
        print(users)
        users = list(filter(lambda user: False if user.get("channel_name") == channel_name else True,users))
        print(users)
        self.users_in = dumps(users)
        self.save()
    
    def new_admin(self):
        users = loads(self.users_in)
        if len(users) < 1:
            self.delete()
            return
        self.admin = users[0]["channel_name"]
        self.save()
        return self.admin
    
    def await_user(self, user):
        waiting_users = loads(self.waiting_users)
        waiting_users.append(user.__dict__())
        self.waiting_users = dumps(waiting_users)
        self.save()
    
    def public_users(self):
        users = loads(self.users_in)
        for user in users:
            user.pop('channel_name')
        return users
