from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LogsViewSet

router = DefaultRouter()
router.register(r'', LogsViewSet, basename='logs')

urlpatterns = [
    path('', include(router.urls)),
]
