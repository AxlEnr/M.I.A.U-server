from rest_framework import serializers
from .models import User, UsersProfile
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny, IsAuthenticated

class UsersProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersProfile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    user_profile = UsersProfileSerializer(read_only=True)

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
            'profile_picture',
            'user_profile',
            'password'
        ]
        extra_kwargs = {'password': {'write_only': True,
        'required': False,
        'allow_null': True,
        'allow_blank': True}}

    def get_permissions(self):
        if self.action in ['create', 'login', 'reset_password', 'signup']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.password = make_password(password)
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
