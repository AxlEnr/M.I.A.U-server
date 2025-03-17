from django.urls import path
from . import views

urlpatterns = [
    # Chats URLs
    path('chats/', views.chats_list, name='chats_list'),
    path('chats/<uuid:chat_id>/', views.chats_detail, name='chats_detail'),

]