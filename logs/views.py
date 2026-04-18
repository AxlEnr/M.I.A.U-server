from rest_framework import viewsets, status, permissions
from .models import Logs
from .serializers import LogsSerializer
from miau_backend.response import ApiResponse

class LogsViewSet(viewsets.ModelViewSet):
    queryset = Logs.objects.all()
    serializer_class = LogsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Logs.objects.all()
        return Logs.objects.filter(userId=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.userId != request.user and not request.user.is_superuser:
            return ApiResponse.error("No tienes permiso para ver este log", status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance)
        return ApiResponse.success(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(userId=request.user)
            return ApiResponse.success(serializer.data, status.HTTP_201_CREATED)
        return ApiResponse.error(serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.userId != request.user and not request.user.is_superuser:
            return ApiResponse.error("No tienes permiso para editar este log", status.HTTP_403_FORBIDDEN)
        return ApiResponse.error("Los logs no pueden ser editados", status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.userId != request.user and not request.user.is_superuser:
            return ApiResponse.error("No tienes permiso para eliminar este log", status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return ApiResponse.success('Log eliminado exitosamente', status.HTTP_204_NO_CONTENT)
