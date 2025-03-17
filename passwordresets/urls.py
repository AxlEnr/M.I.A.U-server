from django.urls import path
from . import views

urlpatterns = [
    # PasswordResets URLs
    path('password-resets/', views.password_resets_list, name='password_resets_list'),
    path('password-resets/<uuid:reset_id>/', views.password_resets_detail, name='password_resets_detail'),
]