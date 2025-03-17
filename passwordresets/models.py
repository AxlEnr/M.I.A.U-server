from django.db import models
from django.contrib.auth.hashers import make_password
import uuid
from user.models import User

class PasswordResets(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    resetToken = models.CharField(max_length=100)
    expiration = models.DateTimeField()
