from django.urls import path
from . import views

urlpatterns = [
    # Comments URLs
    path('comments/', views.comments_list, name='comments_list'),
    path('comments/<uuid:comment_id>/', views.comments_detail, name='comments_detail'),
]