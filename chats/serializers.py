# serializers.py (en tu aplicación chat)
from rest_framework import serializers
from .models import Chat, Message
from user_api.serializers import UserSerializer

class ChatCreateSerializer(serializers.Serializer):
    participant_id = serializers.IntegerField()

    def create(self, validated_data):
        return Chat.objects.create()  # La lógica real está en la vista

class ChatSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'participants', 'last_message', 'unread_count', 'created_at']

    def get_last_message(self, obj):
        # Accede a las relaciones prefetch para mejorar rendimiento
        messages = obj.messages.all()
        if messages.exists():
            last_message = messages.order_by('-timestamp').first()
            return {
                'content': last_message.content,
                'timestamp': last_message.timestamp,
                'sender': UserSerializer(last_message.sender).data
            }
        return None

class ChatDetailSerializer(ChatSerializer):
    messages = serializers.SerializerMethodField()

    class Meta(ChatSerializer.Meta):
        fields = ChatSerializer.Meta.fields + ['messages']

    def get_messages(self, obj):
        messages = obj.messages.order_by('timestamp')
        return MessageSerializer(messages, many=True).data

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'content', 'sender', 'timestamp', 'read', 'read_at']

class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content']