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
from pet.serializers import PetSerializer
from imgspost.serializers import ImgsPostSerializer
from pet.models import Pet
from imgspost.models import ImgsPost

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
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
        
    if request.method == 'POST':
        pet_id = request.data.get('petId')
        try:
            pet = Pet.objects.get(id=pet_id, userId=request.user)
        except Pet.DoesNotExist:
            return Response(
                {'error': 'La mascota no existe o no te pertenece'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Añadir ubicación de la mascota al post si no se proporciona
        post_data = request.data.copy()
        if 'state' not in post_data:
            post_data['state'] = pet.state
        if 'city' not in post_data:
            post_data['city'] = pet.city
            
        serializer = PostSerializer(data=post_data)
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

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_posts(request):
    posts = Post.objects.filter(userId=request.user)
    post_serializer = PostSerializer(posts, many=True)

    pet_ids = [post.petId.id for post in posts]
    pets = Pet.objects.filter(id__in=pet_ids)
    pet_serializer = PetSerializer(pets, many=True)
    
    post_ids = [post.id for post in posts]
    images = ImgsPost.objects.filter(idPost__in=post_ids)
    image_serializer = ImgsPostSerializer(images, many=True)
    
    return Response({
        'posts': post_serializer.data,
        'pets': pet_serializer.data,
        'images': image_serializer.data,
    })