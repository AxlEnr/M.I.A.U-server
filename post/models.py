# posts/models.py
from django.db import models
from django.contrib.auth.hashers import make_password
from user.models import User
from pet.models import Pet

class Post(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=254)
    postDate = models.DateField()
    petId = models.ForeignKey(Pet, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=100, blank=True, null=True)  # Nuevo campo
    city = models.CharField(max_length=100, blank=True, null=True)   # Nuevo campo

    def __str__(self):
        return self.title