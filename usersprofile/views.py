from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import UsersProfile
from .serializers import UsersProfileSerializer

@api_view(['GET', 'POST'])
def users_profile_list(request):
    if request.method == 'GET':
        user_id = request.query_params.get('user_id')  # Obtener el ID del usuario desde los parámetros de la solicitud
        if user_id:
            profiles = UsersProfile.objects.filter(userId_id=user_id)  # Filtrar por ID de usuario
        else:
            profiles = UsersProfile.objects.all()
        serializer = UsersProfileSerializer(profiles, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        user_id = request.data.get('userId')  # Obtener el ID del usuario desde los datos de la solicitud

        # Verificar si el perfil ya existe
        try:
            profile = UsersProfile.objects.get(userId_id=user_id)
            # Si el perfil ya existe, eliminar la imagen anterior antes de actualizar
            if profile.profilePhoto:  # Verificar si hay una imagen anterior
                profile.profilePhoto.delete()  # Eliminar la imagen anterior
            # Actualizar el perfil con los nuevos datos
            serializer = UsersProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
        except UsersProfile.DoesNotExist:
            # Si el perfil no existe, crearlo
            serializer = UsersProfileSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)  # Imprime los errores para depuración
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def users_profile_detail(request, user_id):
    try:
        profile = UsersProfile.objects.get(userId_id=user_id)  # Filtrar por ID de usuario
        if request.method == 'GET':
            serializer = UsersProfileSerializer(profile, context={'request': request})
            return Response(serializer.data)
        elif request.method == 'PUT':
            # Eliminar la imagen anterior antes de actualizar
            if profile.profilePhoto:  # Verificar si hay una imagen anterior
                profile.profilePhoto.delete()  # Eliminar la imagen anterior
            # Actualizar el perfil con los nuevos datos
            serializer = UsersProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            print(serializer.errors)  # Imprime los errores para depuración
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            # Eliminar la imagen asociada al perfil antes de eliminar el perfil
            if profile.profilePhoto:  # Verificar si hay una imagen
                profile.profilePhoto.delete()  # Eliminar la imagen
            profile.delete()  # Eliminar el perfil
            return Response(status=status.HTTP_204_NO_CONTENT)
    except UsersProfile.DoesNotExist:
        return Response({"error": "Perfil no encontrado"}, status=status.HTTP_404_NOT_FOUND)