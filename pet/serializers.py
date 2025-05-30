# pet/serializers.py
from rest_framework import serializers
from .models import Pet
from user.models import User
from user_api.serializers import UserSerializer  # Asegúrate de tener este serializador

class PetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Asegúrate de que este campo esté correctamente definido
    
    class Meta:
        model = Pet
        fields = [
            'id', 'name', 'age', 'breed', 'size', 'petDetails', 
            'userId', 'statusAdoption', 'qrId', 'user'  # Incluye el campo 'user' aquí
        ]
        read_only_fields = ('userId',)
        extra_kwargs = {
            'qrId': {'required': False}  # Hace que el campo no sea obligatorio
        }
        depth = 1  # Esto incluirá los objetos relacionados anidados
