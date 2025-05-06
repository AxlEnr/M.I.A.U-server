from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Notifications
from .serializers import NotificationsSerializer
from user.models import User
# Notifications Views
@api_view(['GET', 'POST'])
def notifications_list(request):
    if request.method == 'GET':
        notifications = Notifications.objects.all()
        serializer = NotificationsSerializer(notifications, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = NotificationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def notifications_detail(request, notification_id):
    notification = get_object_or_404(Notifications, id=notification_id)
    if request.method == 'GET':
        serializer = NotificationsSerializer(notification)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = NotificationsSerializer(notification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_user_notifications(request, user_id):
    try:
        current_user = request.user
        
        notifications = Notifications.objects.filter(
            userId=user_id,
        ).exclude(
            related_post__userId=current_user.id
        ).order_by('-notiDate')
        
        serializer = NotificationsSerializer(notifications, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_notification(request):
    serializer = NotificationsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notifications, id=notification_id)
    notification.read = True
    notification.save()
    return Response({'status': 'marked as read'})

@api_view(['POST'])
def send_lost_pet_notification(request):
    post_id = request.data.get('post_id')
    pet_name = request.data.get('pet_name')
    user_id = request.data.get('user_id')
    
    if not post_id or not pet_name or not user_id:
        return Response({'error': 'post_id, pet_name and user_id are required'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    try:
        from post.models import Post
        post = Post.objects.get(id=post_id)
        
        # Obtener todos los usuarios excepto el que reportó la mascota
        from django.contrib.auth import get_user_model
        User = get_user_model()
        users = User.objects.exclude(id=user_id)
        
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
        
        return Response({
            'status': 'notifications sent',
            'count': len(notifications)
        }, status=status.HTTP_201_CREATED)
    except Post.DoesNotExist:
        return Response({'error': 'Post no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def send_adoption_pet_notification(request):
    post_id = request.data.get('post_id')
    pet_name = request.data.get('pet_name')
    user_id = request.data.get('user_id')
    
    if not post_id or not pet_name or not user_id:
        return Response({'error': 'post_id, pet_name and user_id are required'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    try:
        from post.models import Post
        post = Post.objects.get(id=post_id)
        
        # Obtener todos los usuarios excepto el que publicó la mascota
        from django.contrib.auth import get_user_model
        User = get_user_model()
        users = User.objects.exclude(id=user_id)
        
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
        
        return Response({
            'status': 'notifications sent',
            'count': len(notifications)
        }, status=status.HTTP_201_CREATED)
    except Post.DoesNotExist:
        return Response({'error': 'Post no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)