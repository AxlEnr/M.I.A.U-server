from rest_framework import viewsets, status, permissions
from .models import AdoptionFilters
from .serializers import AdoptionFiltersSerializer
from miau_backend.response import ApiResponse

class AdoptionFiltersViewSet(viewsets.ModelViewSet):
    queryset = AdoptionFilters.objects.all()
    serializer_class = AdoptionFiltersSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AdoptionFilters.objects.filter(userId=self.request.user)

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
            serializer.save(userId=request.user)
            return ApiResponse.success(serializer.data, status.HTTP_201_CREATED)
        return ApiResponse.error(serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        if instance.userId != request.user:
            return ApiResponse.error("No tienes permiso para editar estos filtros.", status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(serializer.data)
        return ApiResponse.error(serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.userId != request.user:
            return ApiResponse.error("No tienes permiso para eliminar estos filtros.", status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(instance)
        return ApiResponse.success('Filtros de adopción eliminados exitosamente', status.HTTP_204_NO_CONTENT)
