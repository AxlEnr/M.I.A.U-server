from django.db import models
from django.contrib.auth.hashers import make_password
import uuid
from user.models import User

class Logs(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)