from rest_framework import serializers
from .models import StatusHistory

class StatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusHistory
        fields = '__all__'
