from rest_framework import viewsets, status, permissions
from django.shortcuts import get_object_or_404
from .models import StatusHistory
from .serializers import StatusHistorySerializer
from miau_backend.response import ApiResponse

class StatusHistoryViewSet(viewsets.ModelViewSet):
    queryset = StatusHistory.objects.all()
    serializer_class = StatusHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return StatusHistory.objects.all()
        return StatusHistory.objects.filter(petId__userId=user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.petId.userId != request.user and not request.user.is_superuser:
            return ApiResponse.error("No tienes permiso para ver este historial", status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance)
        return ApiResponse.success(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(serializer.data, status=status.HTTP_201_CREATED)
        return ApiResponse.error(serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.petId.userId != request.user and not request.user.is_superuser:
            return ApiResponse.error("No tienes permiso para editar este historial", status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(serializer.data)
        return ApiResponse.error(serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.petId.userId != request.user and not request.user.is_superuser:
            return ApiResponse.error("No tienes permiso para eliminar este historial", status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return ApiResponse.success('Historial de estado eliminado exitosamente', status.HTTP_204_NO_CONTENT)