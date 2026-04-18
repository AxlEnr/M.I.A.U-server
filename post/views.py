from rest_framework import viewsets, status, permissions
from .models import Post
from .serializers import PostSerializer
from miau_backend.response import ApiResponse
from pet.models import Pet

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Post.objects.all()
        if self.action in ['list', 'retrieve']:
            return Post.objects.all()
        return Post.objects.filter(userId=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            pet_id = request.data.get('petId')
            try:
                pet = Pet.objects.get(id=pet_id, userId=request.user)
            except Pet.DoesNotExist:
                return ApiResponse.error('La mascota no existe o no te pertenece.', status.HTTP_400_BAD_REQUEST)
            
            post_data = request.data.copy()
            if 'state' not in post_data and pet.state:
                post_data['state'] = pet.state
            if 'city' not in post_data and pet.city:
                post_data['city'] = pet.city

            serializer = self.get_serializer(data=post_data)
            if serializer.is_valid():
                serializer.save(userId=request.user, petId=pet)
                return ApiResponse.success(serializer.data, status.HTTP_201_CREATED)
            return ApiResponse.error(serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)
        return ApiResponse.error(serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        if instance.userId != request.user and not request.user.is_superuser:
            return ApiResponse.error('No tienes permiso para modificar este post.', status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(serializer.data)
        return ApiResponse.error(serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.userId != request.user and not request.user.is_superuser:
            return ApiResponse.error('No tienes permiso para eliminar este post.', status.HTTP_403_FORBIDDEN)
        
        pet_id = instance.petId.id
        instance.delete()
        
        if not Post.objects.filter(petId=pet_id).exists():
            try:
                pet = Pet.objects.get(id=pet_id)
                pet.delete()
            except Pet.DoesNotExist:
                pass
        
        return ApiResponse.success('Post eliminado exitosamente', status.HTTP_204_NO_CONTENT)
