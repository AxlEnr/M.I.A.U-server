from rest_framework import serializers
from .models import Comments
from user.serializers import UserSerializer
from post.models import Post

class CommentsSerializer(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(read_only=True)
    postId = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comments
        fields = ['id', 'comment', 'created_at', 'postId', 'userId']