# Generated by Django 5.1.6 on 2025-03-12 07:02

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeQR',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('qr_code_url', models.URLField(max_length=254)),
                ('pdf_url', models.URLField(max_length=254)),
                ('creation_date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='AdoptionFilters',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('size', models.CharField(choices=[('Pequeño', 'Pequeño'), ('Mediano', 'Mediano'), ('Grande', 'Grande')], max_length=10)),
                ('ageMin', models.IntegerField()),
                ('ageMax', models.IntegerField()),
                ('state', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('breed', models.CharField(blank=True, max_length=30, null=True)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
        migrations.CreateModel(
            name='Chats',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('dateSent', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('idEmitter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emitter', to='user.user')),
                ('idReceiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='user.user')),
            ],
        ),
        migrations.CreateModel(
            name='EmailVerifications',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('verificationCode', models.CharField(max_length=100)),
                ('expiration', models.DateTimeField()),
                ('verified', models.BooleanField(default=False)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('action', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('notifType', models.CharField(choices=[('Desaparecido_Alrededor', 'Desaparecido Alrededor'), ('Nueva_Mascota', 'Nueva Mascota'), ('Comentario', 'Comentario'), ('Mensaje', 'Mensaje'), ('Otro', 'Otro')], max_length=30)),
                ('message', models.TextField()),
                ('read', models.BooleanField(default=False)),
                ('notiDate', models.DateTimeField(auto_now_add=True)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
        migrations.CreateModel(
            name='PasswordResets',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('resetToken', models.CharField(max_length=100)),
                ('expiration', models.DateTimeField()),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('age', models.IntegerField()),
                ('breed', models.CharField(max_length=30)),
                ('size', models.CharField(choices=[('Pequeño', 'Pequeño'), ('Mediano', 'Mediano'), ('Grande', 'Grande')], max_length=10)),
                ('petDetails', models.CharField(blank=True, max_length=254, null=True)),
                ('qrId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prueba.codeqr')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=254)),
                ('postDate', models.DateField()),
                ('petId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prueba.pet')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
        migrations.CreateModel(
            name='ImgsPost',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('imgURL', models.CharField(max_length=254)),
                ('idPost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prueba.post')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('comment', models.TextField()),
                ('commentDate', models.DateTimeField(auto_now_add=True)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
                ('postId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prueba.post')),
            ],
        ),
        migrations.CreateModel(
            name='StatusHistory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('Con dueño', 'Con dueño'), ('En adopción', 'En adopción'), ('Desaparecido', 'Desaparecido'), ('Robado', 'Robado')], max_length=20)),
                ('newDate', models.DateField()),
                ('petId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prueba.pet')),
            ],
        ),
        migrations.CreateModel(
            name='UsersProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('profilePhotoURL', models.CharField(blank=True, max_length=254, null=True)),
                ('state', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=254)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
    ]
