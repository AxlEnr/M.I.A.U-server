from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StatusHistoryViewSet

router = DefaultRouter()
router.register(r'', StatusHistoryViewSet, basename='statushistory')

urlpatterns = [
    path('', include(router.urls)),
]