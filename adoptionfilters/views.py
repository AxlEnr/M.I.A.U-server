from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import AdoptionFilters
from .serializers import AdoptionFiltersSerializer

# AdoptionFilters Views
@api_view(['GET', 'POST'])
def adoption_filters_list(request):
    if request.method == 'GET':
        filters = AdoptionFilters.objects.all()
        serializer = AdoptionFiltersSerializer(filters, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AdoptionFiltersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def adoption_filters_detail(request, filter_id):
    filter = get_object_or_404(AdoptionFilters, id=filter_id)
    if request.method == 'GET':
        serializer = AdoptionFiltersSerializer(filter)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = AdoptionFiltersSerializer(filter, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        filter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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

# Logs Views
@api_view(['GET', 'POST'])
def logs_list(request):
    if request.method == 'GET':
        logs = Logs.objects.all()
        serializer = LogsSerializer(logs, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = LogsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def logs_detail(request, log_id):
    log = get_object_or_404(Logs, id=log_id)
    if request.method == 'GET':
        serializer = LogsSerializer(log)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = LogsSerializer(log, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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