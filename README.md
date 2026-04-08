# 🐾 MIAU BACKEND DJANGO

Este es el servicio de backend para la plataforma **MIAU**, desarrollado con **Django 5.1**. El proyecto utiliza una arquitectura MVC simplificada y está completamente contenedorizado con **Docker** para asegurar un entorno de desarrollo consistente.

---

## Guía de Instalación y Configuración

Sigue estos pasos para levantar el entorno local en pocos minutos.

### 1. Clonar el repositorio
```bash
git clone <link-del-repositorio>
cd miau-backend
```

### 2. Configurar variables de entorno
El sistema requiere un archivo .env para gestionar credenciales y configuraciones sensibles.
```bash
cp .env.example .env
```
Nota: Abre el archivo .env y asegúrate de configurar correctamente la conexión a la base de datos y tu SECRET_KEY.

### 3. Construcción y despliegue con Docker
El sistema requiere un archivo .env para gestionar credenciales y configuraciones sensibles.
```bash
docker compose up -d --build
```

### 4. Ejecutar migraciones
```bash
# Crear archivos de migración
docker compose exec miau-container python manage.py makemigrations

# Aplicar cambios a la base de datos
docker compose exec miau-container python manage.py migrate
```

### 5. Crear Usuario Administrador
```bash
docker compose exec miau-container python manage.py createsuperuser
```

### NOTAS DE DESARROLLO
Para mantener la integridad del proyecto, sigue estas recomendaciones:
## Estructura de las Apps

    Creación Manual: Directorios como user_api fueron estructurados manualmente. Al crear nuevas APIs, asegúrate de incluir los archivos esenciales: models.py, serializers.py, views.py y urls.py.

    Archivos Init: NUNCA borres los archivos __init__.py. Son los que permiten que Python trate las carpetas como paquetes y los import funcionen correctamente.

## Entorno de Python

    Dependencias: Si instalas una nueva librería, agrégala manualmente al requirements.txt o actualízalo desde un entorno limpio. No incluyas librerías del sistema operativo.

    Carpeta venv: No es necesario (ni recomendable) subir la carpeta venv al repositorio. Docker ignora tu entorno local y construye el suyo propio basado en el archivo Dockerfile.

## Configuración de Nuevas Apps

Cada vez que crees una aplicación nueva, es obligatorio:

    Registrarla en la lista INSTALLED_APPS dentro de miau_backend/settings.py.

    Incluir sus rutas en el archivo urls.py principal ubicado en la carpeta del núcleo (miau_backend/).

### STACK UTILIZADO
Lenguaje: Python 3.13-slim
Framework: Django 5.1
Servidor WSGI: Gunicorn
Contenedores: Docker & Docker Compose 

