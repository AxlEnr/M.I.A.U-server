from django.db import models
from django.contrib.auth.hashers import make_password
import uuid
from user.models import User

class Chats(models.Model):
    message = models.TextField()
    dateSent = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    idEmitter = models.ForeignKey(User, related_name='emitter', on_delete=models.CASCADE)
    idReceiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)