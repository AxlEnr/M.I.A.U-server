from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import EmailVerifications
from .serializers import EmailVerificationsSerializer

# EmailVerifications Views
@api_view(['GET', 'POST'])
def email_verifications_list(request):
    if request.method == 'GET':
        verifications = EmailVerifications.objects.all()
        serializer = EmailVerificationsSerializer(verifications, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = EmailVerificationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def email_verifications_detail(request, verification_id):
    verification = get_object_or_404(EmailVerifications, id=verification_id)
    if request.method == 'GET':
        serializer = EmailVerificationsSerializer(verification)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = EmailVerificationsSerializer(verification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        verification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)