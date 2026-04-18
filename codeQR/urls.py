from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CodeQRViewSet

router = DefaultRouter()
router.register(r'', CodeQRViewSet, basename='codeqr')

urlpatterns = [
    path('', include(router.urls)),
]
