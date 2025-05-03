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
    notifications = Notifications.objects.filter(userId=user_id).order_by('-notiDate')
    serializer = NotificationsSerializer(notifications, many=True)
    return Response(serializer.data)

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

# Nueva función para enviar notificaciones masivas
@api_view(['POST'])
def send_lost_pet_notification(request):
    post_id = request.data.get('post_id')
    pet_name = request.data.get('pet_name')
    user_id = request.data.get('user_id')  # ID del usuario que reportó la mascota
    
    if not post_id or not pet_name:
        return Response({'error': 'post_id and pet_name are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Obtener todos los usuarios excepto el que reportó la mascota
    users = User.objects.exclude(id=user_id)
    
    notifications = []
    for user in users:
        notification = Notifications(
            notifType=Notifications.NotifTypeChoices.DESAPARECIDO_ALREDEDOR,
            message=f"¡Se ha perdido {pet_name}! Ayuda a encontrarla.",
            userId=user,
            related_post_id=post_id
        )
        notifications.append(notification)
    
    # Crear todas las notificaciones en una sola operación
    Notifications.objects.bulk_create(notifications)
    
    return Response({'status': 'notifications sent'}, status=status.HTTP_201_CREATED)
