from user.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'id', 
            'last_login',
            'name', 
            'first_name', 
            'age', 
            'email', 
            'phone_number',
            'street',
            'neighborhood',
            'cp',
            'city',
            'state',
            'country',
            'created_date',
            'status',
            'role',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
            'profile_picture'
        ]
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.password = make_password(password)  # Encriptamos la contraseña manualmente
        user.save()
        return user
    
    def get_profile_picture(self, obj):
        profile = getattr(obj, 'user_profile', None) 
        
        if profile and profile.profilePhoto:
            request = self.context.get('request')
            url = profile.profilePhoto.url
            
            if request:
                return request.build_absolute_uri(url)
            return url
            
        return None