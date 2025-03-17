from rest_framework import serializers
from .models import ImgsPost

class ImgsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImgsPost
        fields = '__all__'