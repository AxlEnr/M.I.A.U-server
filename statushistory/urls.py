from django.urls import path
from . import views

urlpatterns = [
    # StatusHistory URLs
    path('status-history/', views.status_history_list, name='status_history_list'),
    path('status-history/<uuid:history_id>/', views.status_history_detail, name='status_history_detail'),

]