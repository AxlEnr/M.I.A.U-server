from django.urls import path
from . import views

urlpatterns = [
    # Pet URLs
    path('pets/', views.pet_list, name='pet_list'),
    path('pets/<uuid:pet_id>/', views.pet_detail, name='pet_detail'),
]