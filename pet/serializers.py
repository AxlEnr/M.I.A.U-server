from rest_framework import serializers
from .models import Pet

class PetSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    
    class Meta:
        model = Pet
        fields = '__all__'
        extra_kwargs = {
            'image': {'required': False}
        }
