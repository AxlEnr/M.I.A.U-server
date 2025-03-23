from django.db import models
from django.contrib.auth.hashers import make_password
import uuid
from user.models import User

class UsersProfile(models.Model):
    description = models.TextField(blank=True, null=True)
    profilePhoto = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=254)
    userId = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', unique=True)  # Asegurar que sea único