from rest_framework import viewsets, status, permissions
from .models import Pet
from .serializers import PetSerializer
from miau_backend.response import ApiResponse

class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Pet.objects.all()
        if self.action in ['retrieve']:
            return Pet.objects.all()
        return Pet.objects.filter(userId=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.image = enco
            serializer.save(userId=request.user)
            return ApiResponse.success(serializer.data, status.HTTP_201_CREATED)
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
            return ApiResponse.error("No tienes permiso para editar esta mascota.", status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(serializer.data)
        return ApiResponse.error(serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.userId != request.user and not request.user.is_superuser:
            return ApiResponse.error("No tienes permiso para eliminar esta mascota.", status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(instance)
        return ApiResponse.success('Mascota eliminada exitosamente', status.HTTP_204_NO_CONTENT)
