from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import StatusHistory
from .serializers import StatusHistorySerializer

# StatusHistory Views
@api_view(['GET', 'POST'])
def status_history_list(request):
    if request.method == 'GET':
        histories = StatusHistory.objects.all()
        serializer = StatusHistorySerializer(histories, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = StatusHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def status_history_detail(request, history_id):
    history = get_object_or_404(StatusHistory, id=history_id)
    if request.method == 'GET':
        serializer = StatusHistorySerializer(history)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = StatusHistorySerializer(history, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        history.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)