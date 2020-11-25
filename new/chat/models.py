from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Blocked_user(models.Model):
    User = models.ForeignKey(User, models.CASCADE, related_name="user")

    def __str__(self):
        return(self.User.username)

class User_reg(models.Model):
    username = models.CharField('username', max_length = 150)
    password = models.CharField('password', max_length = 128)
    password_c = models.CharField('password_confirm', max_length = 128)

class Chat(models.Model):
    user1 = models.ForeignKey(User, models.CASCADE, related_name="User1")
    user2 = models.ForeignKey(User, models.CASCADE, related_name="User2")

class Message(models.Model):
    chat = models.ForeignKey(Chat, models.CASCADE, related_name="message", default= '')
    pub_date = models.DateTimeField(('Дата сообщения'), default=timezone.now)
    user_from = models.CharField('Sender username', max_length = 150)
    text = models.TextField('Message text')

    def date(self):
        return(self.pub_date.astimezone(timezone.get_default_timezone()).strftime('%d.%m.%Y %H:%M'))

    def new_message(self,id):
        pass
