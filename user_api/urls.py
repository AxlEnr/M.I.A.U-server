from django.urls import path
from . import views


#URLS USER
urlpatterns = [
    path('users/', views.get_all_users),
    path('users/signup/', views.signup_user),
    path('users/update/<int:user_id>/', views.update_data_user),
    path('users/delete/<int:user_id>/', views.delete_user),
]