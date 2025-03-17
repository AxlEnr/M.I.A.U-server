from django.urls import path
from . import views

urlpatterns = [
    # Notifications URLs
    path('notifications/', views.notifications_list, name='notifications_list'),
    path('notifications/<uuid:notification_id>/', views.notifications_detail, name='notifications_detail'),

]