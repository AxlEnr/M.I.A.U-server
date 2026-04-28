from django.db import models
from user.models import User
from post.models import Post

class Comments(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    postId = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        db_table = 'comments_comments'
        ordering = ['-created_at']