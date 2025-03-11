from rest_framework.response import Response
from rest_framework.decorators import api_view
from user.models import User
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404 #Show 404 Errors
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password

#GET ALL USERS IN DB
@api_view(['GET'])
def get_all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#POST USER DATA
@api_view(['POST'])
def signup_user(request):
    serializer = UserSerializer(data=request.data)
    #If is valid, return a successful message
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

#UPDATE USER DATA
@api_view(['PUT'])
def update_data_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

# DEACTIVATE USER
@api_view(['PUT'])
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False  # Desactiva al usuario en lugar de modificar datos
    user.save()
    return Response({'message': 'Usuario desactivado'}, status=status.HTTP_200_OK)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        # Validamos la contraseña usando check_password
        if not check_password(password, user.password):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        # Si las credenciales son correctas, devolvemos una respuesta exitosa
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)