from django.db import models
from django.contrib.auth.hashers import make_password
import uuid
from user.models import User
from post.models import Post

class Comments(models.Model):
    comment = models.TextField()
    commentDate = models.DateTimeField(auto_now_add=True)
    postId = models.ForeignKey(Post, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)