# Generated by Django 5.1.6 on 2025-04-30 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_usersprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(max_length=70, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(max_length=70, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='cp',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.CharField(max_length=70, null=True),
        ),
    ]
