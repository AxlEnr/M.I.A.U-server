from django.db import models
from django.contrib.auth.hashers import make_password
import uuid
from user.models import User

class EmailVerifications(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    verificationCode = models.CharField(max_length=100)
    expiration = models.DateTimeField()
    verified = models.BooleanField(default=False)