from rest_framework import serializers
from .models import EmailVerifications

class EmailVerificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerifications
        fields = '__all__'