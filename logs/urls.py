from django.urls import path
from . import views

urlpatterns = [
    # Logs URLs
    path('logs/', views.logs_list, name='logs_list'),
    path('logs/<uuid:log_id>/', views.logs_detail, name='logs_detail'),
]