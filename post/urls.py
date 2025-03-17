from django.urls import path
from . import views

urlpatterns = [
    # Post URLs
    path('posts/', views.post_list, name='post_list'),
    path('posts/<uuid:post_id>/', views.post_detail, name='post_detail')
]