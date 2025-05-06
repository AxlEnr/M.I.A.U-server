from django.db import models
from django.contrib.auth.hashers import make_password
import uuid
from user.models import User
from post.models import Post

class Notifications(models.Model):
    class NotifTypeChoices(models.TextChoices):
        DESAPARECIDO_ALREDEDOR = 'Desaparecido_Alrededor', 'Desaparecido Alrededor'
        NUEVA_MASCOTA = 'Nueva_Mascota', 'Nueva Mascota'
        COMENTARIO = 'Comentario', 'Comentario'
        MENSAJE = 'Mensaje', 'Mensaje'
        OTRO = 'Otro', 'Otro'

    notifType = models.CharField(max_length=30, choices=NotifTypeChoices.choices)
    message = models.TextField()
    read = models.BooleanField(default=False)
    notiDate = models.DateTimeField(auto_now_add=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    related_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True) 