from django.urls import path
from . import views

urlpatterns = [
    # ImgsPost URLs
    path('imgs-post/', views.imgs_post_list, name='imgs_post_list'),
    path('imgs-post/<uuid:img_id>/', views.imgs_post_detail, name='imgs_post_detail'),
    path('imgs-post/by-post/<int:post_id>/', views.imgs_by_post, name='imgs_post_detail'),
]