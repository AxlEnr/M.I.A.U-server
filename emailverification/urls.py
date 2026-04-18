from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmailVerificationsViewSet

router = DefaultRouter()
router.register(r'', EmailVerificationsViewSet, basename='emailverification')

urlpatterns = [
    path('', include(router.urls)),
]
