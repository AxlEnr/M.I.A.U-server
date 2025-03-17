from django.urls import path
from . import views

urlpatterns = [
    # EmailVerifications URLs
    path('email-verifications/', views.email_verifications_list, name='email_verifications_list'),
    path('email-verifications/<uuid:verification_id>/', views.email_verifications_detail, name='email_verifications_detail'),
]