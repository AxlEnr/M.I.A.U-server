from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Prefetch, Q, Count, Max
from django.utils import timezone
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer, MessageCreateSerializer
from user.models import User



class ChatListCreateView(generics.ListCreateAPIView):  # Cambiado a ListCreateAPIView
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(participants=user)\
            .prefetch_related('participants')\
            .annotate(
                last_message_time=Max('messages__timestamp'),
                unread_count=Count(
                    'messages',
                    filter=Q(messages__read=False) & ~Q(messages__sender=user)
                )
            )\
            .order_by('-last_message_time')

    def create(self, request, *args, **kwargs):
        participant_id = request.data.get('participant_id')
        try:
            participant = User.objects.get(id=participant_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        if participant == request.user:
            return Response(
                {'error': 'No puedes chatear contigo mismo'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        existing_chat = Chat.objects.filter(participants=request.user)\
            .filter(participants=participant).first()
        
        if existing_chat:
            serializer = self.get_serializer(existing_chat)
            return Response(serializer.data, status=status.HTTP_200_OK)

        chat = Chat.objects.create()
        chat.participants.add(request.user, participant)
        serializer = self.get_serializer(chat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ChatListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(participants=user)\
            .prefetch_related('participants')\
            .annotate(
                last_message_time=Max('messages__timestamp'),
                unread_count=Count(
                    'messages',
                    filter=Q(messages__read=False) & ~Q(messages__sender=user)
                )
            )\
            .order_by('-last_message_time')

class ChatCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    def create(self, request, *args, **kwargs):
        participant_id = request.data.get('participant_id')
        try:
            participant = User.objects.get(id=participant_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        if participant == request.user:
            return Response(
                {'error': 'No puedes chatear contigo mismo'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        existing_chat = Chat.objects.filter(participants=request.user)\
            .filter(participants=participant).first()
        
        if existing_chat:
            serializer = self.get_serializer(existing_chat)
            return Response(serializer.data, status=status.HTTP_200_OK)

        chat = Chat.objects.create()
        chat.participants.add(request.user, participant)
        serializer = self.get_serializer(chat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(
            chat_id=self.kwargs['chat_id'],
            chat__participants=self.request.user
        ).select_related('sender').order_by('timestamp')

class MessageCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = MessageCreateSerializer

    def perform_create(self, serializer):
        chat = Chat.objects.get(
            id=self.kwargs['chat_id'],
            participants=self.request.user
        )
        serializer.save(chat=chat, sender=self.request.user)

class MarkMessagesAsReadView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        messages = Message.objects.filter(
            chat_id=kwargs['chat_id'],
            chat__participants=self.request.user,
            read=False
        ).exclude(sender=self.request.user)
        
        updated = messages.update(read=True, read_at=timezone.now())
        return Response(
            {'updated_count': updated},
            status=status.HTTP_200_OK
        )