from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import ImgsPost
from .serializers import ImgsPostSerializer
from miau_backend.response import ApiResponse

class ImgsPostViewSet(viewsets.ModelViewSet):
    queryset = ImgsPost.objects.all()
    serializer_class = ImgsPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ImgsPost.objects.all()
        return ImgsPost.objects.filter(idPost__userId=user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.idPost.userId != request.user and not request.user.is_superuser:
            return ApiResponse.error("No tienes permiso para ver esta imagen", status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance)
        return ApiResponse.success(serializer.data)

    def create(self, request, *args, **kwargs):
        post_id = request.data.get('idPost')
        if not post_id:
            return ApiResponse.error("El idPost es obligatorio", status.HTTP_400_BAD_REQUEST)
        from post.models import Post
        try:
            post = Post.objects.get(id=post_id)
            if post.userId != request.user:
                return ApiResponse.error("No tienes permiso para agregar imágenes a este post", status.HTTP_403_FORBIDDEN)
        except Post.DoesNotExist:
            return ApiResponse.error("El post no existe", status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(idPost=post)
            return ApiResponse.success(serializer.data, status=status.HTTP_201_CREATED)
        return ApiResponse.error(serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.idPost.userId != request.user and not request.user.is_superuser:
            return ApiResponse.error("No tienes permiso para editar esta imagen", status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(serializer.data)
        return ApiResponse.error(serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.idPost.userId != request.user and not request.user.is_superuser:
            return ApiResponse.error("No tienes permiso para eliminar esta imagen", status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return ApiResponse.success('Imagen eliminada exitosamente', status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='by-post/(?P<post_id>[^/.]+)')
    def imgs_by_post(self, request, post_id=None):
        images = ImgsPost.objects.filter(idPost=post_id).order_by('-id')
        serializer = self.get_serializer(images, many=True)
        return ApiResponse.success(serializer.data)
