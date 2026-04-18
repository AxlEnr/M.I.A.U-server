from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PasswordResetsViewSet

router = DefaultRouter()
router.register(r'', PasswordResetsViewSet, basename='passwordresets')

urlpatterns = [
    path('', include(router.urls)),
]
