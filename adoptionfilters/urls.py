from django.urls import path
from . import views

urlpatterns = [
    # AdoptionFilters URLs
    path('adoption-filters/', views.adoption_filters_list, name='adoption_filters_list'),
    path('adoption-filters/<uuid:filter_id>/', views.adoption_filters_detail, name='adoption_filters_detail'),

]