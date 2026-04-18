from rest_framework import serializers
from .models import Comments
from user.serializers import UserSerializer
from post.serializers import PostSerializer
from user.models import User
from post.models import Post

class CommentsSerializer(serializers.ModelSerializer):
    userId = UserSerializer(read_only=True)
    userId_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='userId',
        write_only=True,
        required=False
    )
    postId = PostSerializer(read_only=True)
    postId_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(),
        source='postId',
        write_only=True,
        required=True
    )

    class Meta:
        model = Comments
        fields = ['id', 'comment', 'commentDate', 'postId', 'postId_id', 'userId', 'userId_id']
        read_only_fields = ['commentDate']

    def to_internal_id(self, data):
        return data.get('id')
