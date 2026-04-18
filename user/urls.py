from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UsersProfileViewSet, CustomTokenRefreshView

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')
router.register(r'profiles', UsersProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
