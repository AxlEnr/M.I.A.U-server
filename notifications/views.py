from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Notifications
from .serializers import NotificationsSerializer

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
