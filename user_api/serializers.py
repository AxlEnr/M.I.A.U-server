from rest_framework import serializers
from user.models import User

#SERIALIZER
#No entendi muy bien pa que es en el video bro pero tu agregalo
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'