from django.urls import path
from . import views

urlpatterns = [
    # UsersProfile URLs
    path('users-profile/', views.users_profile_list, name='users_profile_list'),
    path('users-profile/<uuid:profile_id>/', views.users_profile_detail, name='users_profile_detail'),
]