from django.db import models
from django.contrib.auth.hashers import make_password
import uuid
from user.models import User
from pet.models import Pet

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=254)
    postDate = models.DateField()
    petId = models.ForeignKey(Pet, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)