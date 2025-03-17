from django.db import models
from django.contrib.auth.hashers import make_password
import uuid
from user.models import User

class UsersProfile(models.Model):
    description = models.TextField(blank=True, null=True)
    profilePhotoURL = models.CharField(max_length=254, blank=True, null=True)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=254)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)