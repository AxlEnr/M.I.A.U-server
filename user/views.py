from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
import random
import string
import logging

from .models import User, UsersProfile
from .serializers import UserSerializer, UsersProfileSerializer
from miau_backend.response import ApiResponse

logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'login', 'reset_password']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return ApiResponse.success(serializer.data, status.HTTP_201_CREATED)
        return ApiResponse.error(serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        if request.user.id != instance.id and not request.user.is_superuser:
            return ApiResponse.error("No tienes permisos para editar este usuario", status.HTTP_403_FORBIDDEN)

        # Handle profile photo if provided
        if 'profilePhoto' in request.FILES:
            user_profile, _ = UsersProfile.objects.get_or_create(user=instance)
            user_profile.profilePhoto = request.FILES['profilePhoto']
            user_profile.save()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return ApiResponse.success(serializer.data)
        return ApiResponse.error(serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.id != instance.id and not request.user.is_superuser:
            return ApiResponse.error("No tienes permisos para eliminar este usuario", status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(instance)
        return ApiResponse.success('Usuario eliminado permanentemente', status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                return ApiResponse.error("Credenciales inválidas", status.HTTP_400_BAD_REQUEST)
            if not user.is_active:
                return ApiResponse.error("Tu usuario está inactivo", status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return ApiResponse.error("Credenciales inválidas", status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        user_data = self.get_serializer(user).data

        return ApiResponse.success({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": user_data 
        })

    @action(detail=False, methods=['post'])
    def logout(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return ApiResponse.success("Cierre de sesión correcto")
            return ApiResponse.error("Token requerido", status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return ApiResponse.error(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return ApiResponse.success(serializer.data)

    @action(detail=False, methods=['post'], url_path='reset-password')
    def reset_password(self, request):
        email = request.data.get('email')
        if not email:
            return ApiResponse.error("El correo electrónico es requerido", status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            user.password = make_password(new_password)
            user.save()
            
            send_mail(
                'Restablecimiento de contraseña - M.I.A.U',
                f'Tu nueva contraseña es: {new_password}\n\nPor favor, cambia esta contraseña después de iniciar sesión.',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return ApiResponse.success("Se ha enviado una nueva contraseña a tu correo electrónico")
        except User.DoesNotExist:
            return ApiResponse.error("No existe un usuario con este correo electrónico", status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return ApiResponse.error(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'], url_path='update-profile-photo')
    def update_profile_photo(self, request):
        try:
            user_profile, _ = UsersProfile.objects.get_or_create(user=request.user)
            if 'profilePhoto' not in request.FILES:
                return ApiResponse.error("No se proporcionó una imagen", status.HTTP_400_BAD_REQUEST)
            
            user_profile.profilePhoto = request.FILES['profilePhoto']
            user_profile.save()
            
            profile_photo_url = request.build_absolute_uri(user_profile.profilePhoto.url)
            return ApiResponse.success({
                "message": "Foto de perfil actualizada exitosamente",
                "profilePhoto": profile_photo_url
            })
        except Exception as e:
            return ApiResponse.error(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

class UsersProfileViewSet(viewsets.ModelViewSet):
    queryset = UsersProfile.objects.all()
    serializer_class = UsersProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(serializer.data)

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return response
        except InvalidToken:
            return ApiResponse.error("Token inválido", status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return ApiResponse.error(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
