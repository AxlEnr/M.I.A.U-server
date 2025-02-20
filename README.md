## MIAU BACKEND DJANGO

### Bajar archivo
`git clone <link>`

### Instalacion

1. Ejecutar maquina virtual: Si estas en Windows `.\miau\venv\Scripts\activate`
2. Instalar requerimientos: `pip install django djangorestframework`

### Comandos importantes

1. Ejecutar servidor `python manage.py runserver`
2. Crear direcorio para trabajar modelos, tests y vistas (Conocidos en django como apps) `python manage.py startapp <nombre>`

### Migrar BD
1. Ejecutar `python manage.py makemigrations`
2. Ejecutar `python manage.py migrate`

#### Nota
Directorios como iser_api fueron creados a mano, creando los 4 archivos mostrados manualmente, por lo que es importante observar como se hicieron

#### Nota 2 
No borrar ningun archivo del venv o de ni de miau_backend o puede dejar de funcionar la app

#### Nota 3
No borrar los __init__ pues son necesarios para que funcione cada app creada

#### Nota 4
No olvidar agregar las apps en el INSTALLED_APPS de wsgi.py en miau_backend para que funcione, ademas de agregar los paths