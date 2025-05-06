from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Post
from pet.models import Pet
from .serializers import PostSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication 
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def get_user_pets(request, user_id):
    """Obtener mascotas de un usuario para crear publicaciones"""
    pets = Pet.objects.filter(userId=user_id)
    data = [{
        'id': pet.id,
        'name': pet.name,
        'age': pet.age,
        'breed': pet.breed,
        'size': pet.size,
        'status': pet.statusAdoption
    } for pet in pets]
    return Response(data)

@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Verificar que la mascota pertenece al usuario
        pet_id = request.data.get('petId')
        try:
            pet = Pet.objects.get(id=pet_id, userId=request.user)
        except Pet.DoesNotExist:
            return Response(
                {'error': 'La mascota no existe o no te pertenece'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(userId=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Permitir a cualquier usuario autenticado ver el post
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method in ['PUT', 'DELETE']:
        # Solo el dueño puede modificar o eliminar
        if post.userId != request.user:
            return Response(
                {'error': 'No tienes permiso para esta acción'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if request.method == 'PUT':
            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            # Verificar si hay otras publicaciones para esta mascota
            pet = post.petId
            post.delete()
            
            if not Post.objects.filter(petId=pet.id).exists():
                # Solo eliminar la mascota si no tiene otras publicaciones
                pet.delete()
                
            return Response(status=status.HTTP_204_NO_CONTENT)