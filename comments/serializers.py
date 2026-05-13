from rest_framework import serializers
from .models import Comments
from post.models import Post

class CommentsSerializer(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(read_only=True)
    postId = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    user_name = serializers.SerializerMethodField(read_only=True)
    user_profile_photo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comments
        fields = ['id', 'comment', 'created_at', 'postId', 'userId',
                  'user_name', 'user_profile_photo']

    def get_user_name(self, obj):
        if obj.userId:
            return f"{obj.userId.name} {obj.userId.first_name}".strip()
        return "Usuario desconocido"

    def get_user_profile_photo(self, obj):
        request = self.context.get('request')
        if obj.userId:
            profile = getattr(obj.userId, 'user_profile', None)
            if profile and profile.profilePhoto:
                url = profile.profilePhoto.url
                if request:
                    return request.build_absolute_uri(url)
                return url
        return None