from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.notifications_list, name='notifications_list'),
    path('notifications/<uuid:notification_id>/', views.notifications_detail, name='notifications_detail'),
    path('notifications/user/<int:user_id>/', views.get_user_notifications, name='user_notifications'),
    path('notifications/create/', views.create_notification, name='create_notification'),
    path('notifications/mark-read/<uuid:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('notifications/send-lost-pet/', views.send_lost_pet_notification, name='send_lost_pet_notification'),
]