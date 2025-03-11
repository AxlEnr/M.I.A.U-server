from django.urls import path
from . import views
from .views import LoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

#URLS USER
urlpatterns = [
    path('users/', views.get_all_users),
    path('users/signup/', views.signup_user),
    path('users/update/<int:user_id>/', views.update_data_user),
    path('users/delete/<int:user_id>/', views.delete_user),
    path('users/login/', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]