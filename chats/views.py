from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Chats
from .serializers import ChatsSerializer

# Chats Views
@api_view(['GET', 'POST'])
def chats_list(request):
    if request.method == 'GET':
        chats = Chats.objects.all()
        serializer = ChatsSerializer(chats, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ChatsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def chats_detail(request, chat_id):
    chat = get_object_or_404(Chats, id=chat_id)
    if request.method == 'GET':
        serializer = ChatsSerializer(chat)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ChatsSerializer(chat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        chat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)