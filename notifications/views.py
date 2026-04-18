from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Notifications
from .serializers import NotificationsSerializer
from user.models import User
from miau_backend.response import ApiResponse

class NotificationsViewSet(viewsets.ModelViewSet):
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Notifications.objects.all()
        return Notifications.objects.filter(userId=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.userId != request.user and not request.user.is_superuser:
            return ApiResponse.error("No tienes permiso para ver esta notificación", status.HTTP_403_FORBIDDEN)
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
        if instance.userId != request.user and not request.user.is_superuser:
            return ApiResponse.error("No tienes permiso para editar esta notificación", status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(serializer.data)
        return ApiResponse.error(serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.userId != request.user and not request.user.is_superuser:
            return ApiResponse.error("No tienes permiso para eliminar esta notificación", status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return ApiResponse.success('Notificación eliminada exitosamente', status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def user_notifications(self, request):
        try:
            notifications = Notifications.objects.filter(
                userId=request.user,
            ).exclude(
                related_post__userId=request.user.id
            ).order_by('-notiDate')
            
            serializer = self.get_serializer(notifications, many=True)
            return ApiResponse.success(serializer.data)
        except Exception as e:
            return ApiResponse.error(str(e), status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        if notification.userId != request.user and not request.user.is_superuser:
            return ApiResponse.error("No tienes permiso para modificar esta notificación", status.HTTP_403_FORBIDDEN)
        notification.read = True
        notification.save()
        return ApiResponse.success({'status': 'marked as read'})
    @action(detail=False, methods=['post'])
    def send_lost_pet_notification(self, request):
        post_id = request.data.get('post_id')
        pet_name = request.data.get('pet_name')
        # user_id is implicit from request.user
        
        if not post_id or not pet_name:
            return ApiResponse.error({'error': 'post_id and pet_name are required'}, 
                                   status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from post.models import Post # Import here to avoid circular dependencies if Post also imports Notifications
            post = Post.objects.get(id=post_id)
            
            from django.contrib.auth import get_user_model
            User = get_user_model()
            # Obtener todos los usuarios excepto el que reportó la mascota
            users = User.objects.exclude(id=request.user.id)
            
            notifications = []
            for user in users:
                notification = Notifications(
                    notifType=Notifications.NotifTypeChoices.DESAPARECIDO_ALREDEDOR,
                    message=f"¡Se ha perdido {pet_name}! Ayuda a encontrarla.",
                    userId=user,
                    related_post=post  # Asociamos el post directamente
                )
                notifications.append(notification)
            
            # Usar bulk_create para mejor performance
            Notifications.objects.bulk_create(notifications)
            
            return ApiResponse.success({
                'status': 'notifications sent',
                'count': len(notifications)
            }, status=status.HTTP_201_CREATED)
        except Post.DoesNotExist:
            return ApiResponse.error({'error': 'Post no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return ApiResponse.error({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def send_adoption_pet_notification(self, request):
        post_id = request.data.get('post_id')
        pet_name = request.data.get('pet_name')
        # user_id is implicit from request.user
        
        if not post_id or not pet_name:
            return ApiResponse.error({'error': 'post_id and pet_name are required'}, 
                                   status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from post.models import Post
            post = Post.objects.get(id=post_id)
            
            from django.contrib.auth import get_user_model
            User = get_user_model()
            users = User.objects.exclude(id=request.user.id)
            
            notifications = []
            for user in users:
                notification = Notifications(
                    notifType=Notifications.NotifTypeChoices.NUEVA_MASCOTA,
                    message=f"¡Nueva mascota en adopción: {pet_name}! ¿Quieres darle un hogar?",
                    userId=user,
                    related_post=post
                )
                notifications.append(notification)
            
            Notifications.objects.bulk_create(notifications)
            
            return ApiResponse.success({
                'status': 'notifications sent',
                'count': len(notifications)
            }, status=status.HTTP_201_CREATED)
        except Post.DoesNotExist:
            return ApiResponse.error({'error': 'Post no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return ApiResponse.error({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)