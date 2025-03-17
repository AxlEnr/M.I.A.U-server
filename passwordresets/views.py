from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import PasswordResets
from .serializers import PasswordResetsSerializer

# PasswordResets Views
@api_view(['GET', 'POST'])
def password_resets_list(request):
    if request.method == 'GET':
        resets = PasswordResets.objects.all()
        serializer = PasswordResetsSerializer(resets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PasswordResetsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def password_resets_detail(request, reset_id):
    reset = get_object_or_404(PasswordResets, id=reset_id)
    if request.method == 'GET':
        serializer = PasswordResetsSerializer(reset)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PasswordResetsSerializer(reset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        reset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)