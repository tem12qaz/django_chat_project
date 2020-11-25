from django.contrib import admin
from .models import Message, Chat, Blocked_user

admin.site.register(Message)
admin.site.register(Chat)
admin.site.register(Blocked_user)
