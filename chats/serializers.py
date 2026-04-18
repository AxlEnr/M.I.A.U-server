from rest_framework import serializers
from .models import Chat, Message
from user.serializers import UserSerializer # Assuming UserSerializer is available in user app

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'

class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content']

class ChatSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    unread_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Chat
        fields = [
            'id',
            'participants',
            'created_at',
            'messages',
            'unread_count',
        ]

class ChatCreateSerializer(serializers.Serializer):
    participant_id = serializers.IntegerField()

