from django.db import models
from django.contrib.auth.hashers import make_password
import uuid
from user.models import User
from post.models import Post

class ImgsPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    imgURL = models.CharField(max_length=254)
    idPost = models.ForeignKey(Post, on_delete=models.CASCADE)

