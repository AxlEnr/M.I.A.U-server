from rest_framework import serializers
from .models import CodeQR  

class CodeQRSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeQR
        fields = '__all__'
