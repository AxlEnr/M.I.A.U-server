# urls.py (backend)

from django.urls import path
from . import views

urlpatterns = [
    path('pets/', views.pet_list, name='pet_list'),
    path('pets/<int:pet_id>/', views.pet_detail, name='pet_detail'),
    path('lost-pets/', views.report_lost_pet, name='report_lost_pet'),
    path('adoption-pets/', views.publish_adoption_pet, name='publish_adoption_pet'),
    path('filtered-pets/', views.pet_list_filtered, name='pet_list_filtered'),
    path('generate-qr/<int:pet_id>/', views.generate_qr_for_pet, name='generate_qr_for_pet'),  # Nueva ruta
    path('qr/delete/<int:pet_id>/', views.delete_qr, name='delete_qr'),
]