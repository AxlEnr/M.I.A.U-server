from rest_framework.response import Response
from rest_framework.decorators import api_view
from user.models import User
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404 #Show 404 Errors
from rest_framework import status

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

#DELETE USER
@api_view(['DELETE'])
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return Response({"message":  "User has been deleted from DB"}, status=status.HTTP_204_NO_CONTENT)
    