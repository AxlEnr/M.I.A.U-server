import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miau_backend.settings')
import django
django.setup()
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'comments_comments'")
for row in cursor.fetchall():
    print(row[0])