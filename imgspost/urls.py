from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImgsPostViewSet

router = DefaultRouter()
router.register(r'', ImgsPostViewSet, basename='imgspost')

urlpatterns = [
    path('', include(router.urls)),
]