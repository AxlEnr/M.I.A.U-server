from django.urls import path
from . import views

urlpatterns = [
    path('qr/', views.get_all_QR),
    path('qr/<int:qr_id>/', views.update_data_QR),
    path('qr/create/', views.create_QR)
]