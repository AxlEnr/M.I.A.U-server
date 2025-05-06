from rest_framework import serializers
from .models import Comments
from django.contrib.auth import get_user_model
from user.models import User

User = get_user_model()

class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = '__all__'

    def get_user(self, obj):
        try:
            user = User.objects.get(id=obj.userId.id)
            return {
                "id": user.id,
                "name": user.name + " " + user.first_name 
            }
        except User.DoesNotExist:
            return {
                "id": None,
                "name": "Usuario no encontrado"
            }
