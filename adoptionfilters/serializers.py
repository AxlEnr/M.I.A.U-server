from rest_framework import serializers
from .models import AdoptionFilters

class AdoptionFiltersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptionFilters
        fields = '__all__'