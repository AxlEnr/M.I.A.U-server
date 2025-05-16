from django.urls import path
from . import views
from .views import LoginView, CustomTokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# URLS DE USUARIO
urlpatterns = [
    path('users/', views.get_all_users),
    path('users/<int:user_id>/', views.get_user_by_id),
    path('users/me/', views.get_logged_in_user), 
    path('users/signup/', views.signup_user),
    path('users/update/<int:user_id>/', views.update_data_user),
    path('users/delete/<int:user_id>/', views.delete_user),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/logout/', views.logout, name='logout'), 
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('users/reset-password/', views.reset_password, name='reset-password'),
    path('users/update-profile-photo/', views.update_profile_photo, name='update_profile_photo'),
]