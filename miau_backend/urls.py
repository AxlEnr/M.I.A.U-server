from django.contrib import admin  # Importar el módulo admin
from django.urls import path, include
from django.http import HttpResponse  # Importar HttpResponse
from django.conf import settings  # Importar settings
from django.conf.urls.static import static  # Importar static

# Vista simple para la URL raíz
def home(request):
    return HttpResponse("¡Bienvenido a la API de Miau Backend!")

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Ruta para la URL raíz
    path('', home, name='home'),
    
    # Rutas de las aplicaciones
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

# Servir archivos multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)