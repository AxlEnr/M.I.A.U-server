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
    path('api/', include('miau_backend.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)