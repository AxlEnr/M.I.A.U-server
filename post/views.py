from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Post
from .serializers import PostSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication 
from rest_framework.permissions import IsAuthenticated


@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id, userId=request.user)  # Solo el dueño puede editar/borrar
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Eliminar también la mascota asociada si no tiene otras publicaciones
        pet = post.petId
        post.delete()
        
        # Verificar si hay otras publicaciones para esta mascota
        if not Post.objects.filter(petId=pet.id).exists():
            pet.delete()
            
        return Response(status=status.HTTP_204_NO_CONTENT)