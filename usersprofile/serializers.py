from rest_framework import serializers
from .models import UsersProfile

class UsersProfileSerializer(serializers.ModelSerializer):
    profilePhoto = serializers.SerializerMethodField()

    class Meta:
        model = UsersProfile
        fields = ['id', 'description', 'profilePhoto', 'state', 'city', 'address', 'userId']

    def get_profilePhoto(self, obj):
        if obj.profilePhoto:
            return obj.profilePhoto.url  # Devuelve la URL relativa
        return None