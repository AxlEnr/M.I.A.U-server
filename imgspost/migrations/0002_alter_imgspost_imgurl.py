# Generated by Django 5.1.6 on 2025-03-23 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imgspost', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imgspost',
            name='imgURL',
            field=models.ImageField(upload_to='post_images/'),
        ),
    ]
