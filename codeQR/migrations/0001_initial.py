# Generated by Django 5.1.6 on 2025-03-17 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CodeQR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr_code_url', models.URLField(max_length=254)),
                ('pdf_url', models.URLField(max_length=254)),
                ('creation_date', models.DateField(auto_now=True)),
            ],
        ),
    ]
