from rest_framework import serializers
from .models import UsersProfile

class UsersProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersProfile
        fields = '__all__'