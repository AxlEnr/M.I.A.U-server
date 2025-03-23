from rest_framework import serializers
from .models import Post
from user.models import UsersProfile  # Importación corregida

class PostSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'postDate', 'petId', 'userId', 'user_name', 'user_profile_photo']

    def get_user_name(self, obj):
        return obj.userId.name  # Suponiendo que el modelo User tiene un campo 'name'

    def get_user_profile_photo(self, obj):
        try:
            profile = UsersProfile.objects.get(user=obj.userId)
            if profile.profilePhoto:
                return self.context['request'].build_absolute_uri(profile.profilePhoto.url)
        except UsersProfile.DoesNotExist:
            pass
        return None