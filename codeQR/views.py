from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import CodeQR
from .serializer import CodeQRSerializer
from django.shortcuts import get_object_or_404 #Show 404 Errors
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

#GET ALL USERS IN DB
@api_view(['GET'])
def get_all_QR(request):
    qr = CodeQR.objects.all()
    serializer = CodeQRSerializer(qr, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#UPDATE USER DATA
@api_view(['PUT'])
def update_data_QR(request, qr_id ):
    qr = get_object_or_404(CodeQR, id=qr_id)
    serializer = CodeQRSerializer(qr, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def delete_QR(request, qr_id):
    qr = get_object_or_404(qr, id=qr_id)
    qr.delete()
    return Response({'message': 'Codigo QR desactivado'}, status=status.HTTP_200_OK)

#POST USER DATA
@api_view(['POST'])
def create_QR(request):
    serializer = CodeQRSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Devuelve los errores del serializador
