from django.urls import path
from .views import (
    ChatCreateView,
    MessageListView,
    MessageCreateView,
    MarkMessagesAsReadView,
    ChatListCreateView
)

urlpatterns = [
    path('', ChatListCreateView.as_view(), name='chat-list'),
    path('create/', ChatListCreateView.as_view(), name='chat-create'),
    path('<int:chat_id>/messages/', MessageListView.as_view(), name='message-list'),
    path('<int:chat_id>/messages/create/', MessageCreateView.as_view(), name='message-create'),
    path('<int:chat_id>/mark-read/', MarkMessagesAsReadView.as_view(), name='mark-messages-read'),
]