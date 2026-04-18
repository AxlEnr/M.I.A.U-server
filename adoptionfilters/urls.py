from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdoptionFiltersViewSet

router = DefaultRouter()
router.register(r'', AdoptionFiltersViewSet, basename='adoptionfilters')

urlpatterns = [
    path('', include(router.urls)),
]
