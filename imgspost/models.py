from django.db import models
from post.models import Post

class ImgsPost(models.Model):
    imgURL = models.ImageField(upload_to='post_images/')  # Cambia a ImageField
    idPost = models.ForeignKey(Post, on_delete=models.CASCADE)