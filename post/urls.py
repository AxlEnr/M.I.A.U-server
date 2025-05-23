from django.urls import path
from . import views

urlpatterns = [
    # Post URLs
    path('posts/', views.post_list, name='post_list'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('pets/user/<int:user_id>/', views.get_user_pets),
    path('user/posts/', views.user_posts, name='user_posts'),
]