from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import InvalidToken
from user.models import User, UsersProfile
from .serializers import UserSerializer
import logging

logger = logging.getLogger(__name__)

# 🔹 LOGIN Y GENERACIÓN DE TOKEN
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):  # Verificar la contraseña
                return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
            if not user.is_active:
                return Response({"error": "User is not active"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        # 🔹 Generamos los tokens
        refresh = RefreshToken.for_user(user)

        # 🔹 Serializamos el usuario para devolver sus datos
        user_data = UserSerializer(user).data

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": user_data  # Incluimos los datos del usuario
        }, status=status.HTTP_200_OK)

# 🔹 OBTENER USUARIO DE LA SESIÓN ACTUAL (Requiere autenticación)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_logged_in_user(request):
    try:
        user = request.user  # 🔹 Obtener usuario autenticado
        if not user.is_active:
            return Response({"error": "User is inactive"}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error obteniendo usuario autenticado: {e}")
        return Response({"error": "Error interno del servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 🔹 OBTENER USUARIO POR ID
@api_view(['GET'])
def get_user_by_id(request, user_id):
    user = get_object_or_404(User, id=user_id)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 🔹 OBTENER TODOS LOS USUARIOS
@api_view(['GET'])
def get_all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 🔹 REGISTRAR USUARIO
@api_view(['POST'])
def signup_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 🔹 ACTUALIZAR DATOS DE USUARIO
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_data_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Verifica si el usuario autenticado es el mismo que está intentando actualizar
    if request.user.id != user.id:
        return Response({"error": "No tienes permisos para editar este usuario"}, status=status.HTTP_403_FORBIDDEN)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 🔹 ELIMINAR USUARIO (desactivar cuenta)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        
        # Verificar que el usuario autenticado es el mismo que se quiere eliminar
        if request.user.id != user.id:
            return Response(
                {"error": "No tienes permisos para eliminar este usuario"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Eliminar el usuario
        user.delete()
        
        return Response(
            {'message': 'Usuario eliminado permanentemente'},
            status=status.HTTP_204_NO_CONTENT
        )
        
    except User.DoesNotExist:
        return Response(
            {"error": "Usuario no encontrado"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# 🔹 REFRESCAR TOKEN
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            if response.status_code == 200:
                return response
            else:
                return Response({"error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
        except InvalidToken as e:
            logger.error(f"Invalid refresh token: {e}")
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.error(f"Error refreshing token: {e}")
            return Response({"error": "Error refreshing token"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import traceback

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        else:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)

    except Exception as e:
        traceback.print_exc()  # Esto mostrará el error completo en consola
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password

@api_view(['POST'])
def reset_password(request):
    email = request.data.get('email')
    
    if not email:
        return Response({"error": "El correo electrónico es requerido"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "No existe un usuario con este correo electrónico"}, status=status.HTTP_404_NOT_FOUND)
    
    new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    user.password = make_password(new_password)
    user.save()
    
    try:
        # Añade logging para verificar las credenciales
        logger.info(f"Intentando enviar email con: {settings.EMAIL_HOST_USER}")
        
        send_mail(
            'Restablecimiento de contraseña - M.I.A.U',
            f'Tu nueva contraseña es: {new_password}\n\nPor favor, cambia esta contraseña después de iniciar sesión.',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        logger.info("Email enviado exitosamente")
        return Response({"message": "Se ha enviado una nueva contraseña a tu correo electrónico"}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error enviando email: {str(e)}", exc_info=True)
        return Response({
            "error": "Ocurrió un error al enviar el correo. Por favor intenta más tarde.",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_profile_photo(request):
    try:
        user_profile, created = UsersProfile.objects.get_or_create(user=request.user)
        
        if 'profilePhoto' not in request.FILES:
            return Response({"error": "No se proporcionó una imagen"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_profile.profilePhoto = request.FILES['profilePhoto']
        user_profile.save()
        
        # Usa request.build_absolute_uri() para generar la URL completa
        profile_photo_url = request.build_absolute_uri(user_profile.profilePhoto.url)
        
        return Response({
            "message": "Foto de perfil actualizada exitosamente",
            "profilePhoto": profile_photo_url  # Envía la URL completa
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error actualizando foto de perfil: {str(e)}")
        return Response(
            {"error": "Error al actualizar la foto de perfil", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )