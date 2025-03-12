from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Pet, StatusHistory, Post, ImgsPost, Comments, Notifications, Chats, AdoptionFilters, UsersProfile, Logs, PasswordResets, EmailVerifications
from .serializers import PetSerializer, StatusHistorySerializer, PostSerializer, ImgsPostSerializer, CommentsSerializer, NotificationsSerializer, ChatsSerializer, AdoptionFiltersSerializer, UsersProfileSerializer, LogsSerializer, PasswordResetsSerializer, EmailVerificationsSerializer

# Pet Views
@api_view(['GET', 'POST'])
def pet_list(request):
    if request.method == 'GET':
        pets = Pet.objects.all()
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'GET':
        serializer = PetSerializer(pet)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PetSerializer(pet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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

# Post Views
@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ImgsPost Views
@api_view(['GET', 'POST'])
def imgs_post_list(request):
    if request.method == 'GET':
        imgs = ImgsPost.objects.all()
        serializer = ImgsPostSerializer(imgs, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ImgsPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def imgs_post_detail(request, img_id):
    img = get_object_or_404(ImgsPost, id=img_id)
    if request.method == 'GET':
        serializer = ImgsPostSerializer(img)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ImgsPostSerializer(img, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        img.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Comments Views
@api_view(['GET', 'POST'])
def comments_list(request):
    if request.method == 'GET':
        comments = Comments.objects.all()
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def comments_detail(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)
    if request.method == 'GET':
        serializer = CommentsSerializer(comment)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CommentsSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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