from rest_framework import serializers
from .models import Post
from user.models import UsersProfile

class PostSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_profile_photo = serializers.SerializerMethodField()
    user_first_name = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_user_name(self, obj):
        return obj.userId.name if obj.userId else None

    def get_user_first_name(self, obj):
        return obj.userId.first_name if obj.userId else None

    def get_user_profile_photo(self, obj):
        try:
            if not obj.userId:
                return None
                
            profile = UsersProfile.objects.get(user=obj.userId)
            if not profile.profilePhoto:
                return None
                
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(profile.profilePhoto.url)
            return profile.profilePhoto.url
        except UsersProfile.DoesNotExist:
            return None