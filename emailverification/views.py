from rest_framework import viewsets, status, permissions
from .models import EmailVerifications
from .serializers import EmailVerificationsSerializer
from miau_backend.response import ApiResponse

class EmailVerificationsViewSet(viewsets.ModelViewSet):
    queryset = EmailVerifications.objects.all()
    serializer_class = EmailVerificationsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return ApiResponse.error("No tienes permiso para ver esta información.", status.HTTP_403_FORBIDDEN)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return ApiResponse.error("No tienes permiso para ver esta información.", status.HTTP_403_FORBIDDEN)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(serializer.data, status.HTTP_201_CREATED)
        return ApiResponse.error(serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)
