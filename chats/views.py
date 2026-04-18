from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from django.db.models import Q, Count, Max
from django.utils import timezone

from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer, MessageCreateSerializer, ChatCreateSerializer
from user.models import User
from miau_backend.response import ApiResponse

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(participants=user) \
            .prefetch_related('participants') \
            .annotate(
                last_message_time=Max('messages__timestamp'),
                unread_count=Count(
                    'messages',
                    filter=Q(messages__read=False) & ~Q(messages__sender=user)
                )
            ) \
            .order_by('-last_message_time')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(serializer.data)

    @action(detail=False, methods=['post'], serializer_class=ChatCreateSerializer)
    def create_chat(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        participant_id = serializer.validated_data['participant_id']

        try:
            participant = User.objects.get(id=participant_id)
        except User.DoesNotExist:
            return ApiResponse.error('Usuario no encontrado', status.HTTP_404_NOT_FOUND)

        if participant == request.user:
            return ApiResponse.error('No puedes chatear contigo mismo', status.HTTP_400_BAD_REQUEST)

        existing_chat = Chat.objects.filter(participants=request.user) \
            .filter(participants=participant).first()
        
        if existing_chat:
            chat_serializer = ChatSerializer(existing_chat)
            return ApiResponse.success(chat_serializer.data, status.HTTP_200_OK)

        chat = Chat.objects.create()
        chat.participants.add(request.user, participant)
        chat_serializer = ChatSerializer(chat)
        return ApiResponse.success(chat_serializer.data, status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            chat_id=self.kwargs['chat_pk'], # Use chat_pk for nested routing
            chat__participants=self.request.user
        ).select_related('sender').order_by('timestamp')

    def create(self, request, *args, **kwargs):
        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            chat = Chat.objects.get(
                id=self.kwargs['chat_pk'],
                participants=self.request.user
            )
        except Chat.DoesNotExist:
            return ApiResponse.error('Chat no encontrado o no autorizado', status.HTTP_404_NOT_FOUND)

        message = serializer.save(chat=chat, sender=request.user)
        response_serializer = self.get_serializer(message)
        return ApiResponse.success(response_serializer.data, status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='mark-read')
    def mark_messages_as_read(self, request, chat_pk=None):
        messages = Message.objects.filter(
            chat_id=chat_pk,
            chat__participants=self.request.user,
            read=False
        ).exclude(sender=self.request.user)
        
        updated = messages.update(read=True, read_at=timezone.now())
        return ApiResponse.success(
            {'updated_count': updated},
            status=status.HTTP_200_OK
        )
