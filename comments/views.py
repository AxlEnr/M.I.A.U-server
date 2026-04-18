from rest_framework import viewsets, status, permissions
from django.shortcuts import get_object_or_404
from .models import Comments
from .serializers import CommentsSerializer
from miau_backend.response import ApiResponse
from post.models import Post # Import Post model to validate postId

class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Comments.objects.all()
        post_id = self.request.query_params.get('postId')
        if post_id:
            queryset = queryset.filter(postId=post_id)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(serializer.data)

    def create(self, request, *args, **kwargs):
        # Ensure the postId exists and the user is authenticated
        post_id = request.data.get('postId')
        if not post_id:
            return ApiResponse.error("El postId es obligatorio", status.HTTP_400_BAD_REQUEST)
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return ApiResponse.error("El post no existe", status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(userId=request.user, postId=post) # Assign authenticated user and validated post
            return ApiResponse.success(serializer.data, status.HTTP_201_CREATED)
        return ApiResponse.error(serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Only the owner can update their comment
        if instance.userId != request.user:
            return ApiResponse.error("No tienes permiso para editar este comentario.", status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(serializer.data)
        return ApiResponse.error(serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Only the owner can delete their comment
        if instance.userId != request.user:
            return ApiResponse.error("No tienes permiso para eliminar este comentario.", status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(instance)
        return ApiResponse.success('Comentario eliminado exitosamente', status.HTTP_204_NO_CONTENT)
