from rest_framework import serializers
from .models import Pet, StatusHistory, Post, ImgsPost, Comments, Notifications, Chats, AdoptionFilters, UsersProfile, Logs, PasswordResets, EmailVerifications


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'

class StatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusHistory
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class ImgsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImgsPost
        fields = '__all__'

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'

class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'

class ChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chats
        fields = '__all__'

class AdoptionFiltersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptionFilters
        fields = '__all__'

class UsersProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersProfile
        fields = '__all__'

class LogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = '__all__'

class PasswordResetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordResets
        fields = '__all__'

class EmailVerificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerifications
        fields = '__all__'