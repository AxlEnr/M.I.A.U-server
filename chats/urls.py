from django.urls import path, include
from rest_framework_nested import routers
from .views import ChatViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'', ChatViewSet, basename='chat')

chats_router = routers.NestedSimpleRouter(router, r'', lookup='chat')
chats_router.register(r'messages', MessageViewSet, basename='chat-message')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(chats_router.urls)),
]
