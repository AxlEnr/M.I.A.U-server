from rest_framework import serializers
from .models import PasswordResets

class PasswordResetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordResets
        fields = '__all__'