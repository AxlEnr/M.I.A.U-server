from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import UsersProfile
from .serializers import UsersProfileSerializer

# UsersProfile Views
@api_view(['GET', 'POST'])
def users_profile_list(request):
    if request.method == 'GET':
        profiles = UsersProfile.objects.all()
        serializer = UsersProfileSerializer(profiles, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UsersProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def users_profile_detail(request, profile_id):
    profile = get_object_or_404(UsersProfile, id=profile_id)
    if request.method == 'GET':
        serializer = UsersProfileSerializer(profile)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UsersProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)