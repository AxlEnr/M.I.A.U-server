"""
URL configuration for miau_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# ROUTES TO ACCESS THE METHODS
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Separar cada include en una línea diferente
    path('api/', include('adoptionfilters.urls')),
    path('api/', include('chats.urls')),
    path('api/', include('codeQR.urls')),
    path('api/', include('comments.urls')),
    path('api/', include('emailverification.urls')),
    path('api/', include('imgspost.urls')),
    path('api/', include('logs.urls')),
    path('api/', include('notifications.urls')),
    path('api/', include('passwordresets.urls')),
    path('api/', include('pet.urls')),
    path('api/', include('post.urls')),
    path('api/', include('statushistory.urls')),
    path('api/', include('user_api.urls')),
    path('api/', include('usersprofile.urls')),
]

