from django.db import models
from django.contrib.auth.hashers import make_password
import uuid
from user.models import User

class CodeQR(models.Model):
    # Options for role field
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    qr_code_url = models.URLField(max_length=254)
    pdf_url = models.URLField(max_length=254)
    creation_date = models.DateField(auto_now=True)


class Pet(models.Model):
    class SizeChoices(models.TextChoices):
        PEQUENO = 'Pequeño', 'Pequeño'
        MEDIANO = 'Mediano', 'Mediano'
        GRANDE = 'Grande', 'Grande'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    breed = models.CharField(max_length=30)
    size = models.CharField(max_length=10, choices=SizeChoices.choices)
    petDetails = models.CharField(max_length=254, blank=True, null=True)
    qrId = models.ForeignKey('CodeQR', on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

class StatusHistory(models.Model):
    class StatusChoices(models.TextChoices):
        CON_DUENO = 'Con dueño', 'Con dueño'
        EN_ADOPCION = 'En adopción', 'En adopción'
        DESAPARECIDO = 'Desaparecido', 'Desaparecido'
        ROBADO = 'Robado', 'Robado'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20, choices=StatusChoices.choices)
    newDate = models.DateField()
    petId = models.ForeignKey(Pet, on_delete=models.CASCADE)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=254)
    postDate = models.DateField()
    petId = models.ForeignKey(Pet, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

class ImgsPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    imgURL = models.CharField(max_length=254)
    idPost = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.TextField()
    commentDate = models.DateTimeField(auto_now_add=True)
    postId = models.ForeignKey(Post, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

class Notifications(models.Model):
    class NotifTypeChoices(models.TextChoices):
        DESAPARECIDO_ALREDEDOR = 'Desaparecido_Alrededor', 'Desaparecido Alrededor'
        NUEVA_MASCOTA = 'Nueva_Mascota', 'Nueva Mascota'
        COMENTARIO = 'Comentario', 'Comentario'
        MENSAJE = 'Mensaje', 'Mensaje'
        OTRO = 'Otro', 'Otro'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notifType = models.CharField(max_length=30, choices=NotifTypeChoices.choices)
    message = models.TextField()
    read = models.BooleanField(default=False)
    notiDate = models.DateTimeField(auto_now_add=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

class Chats(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.TextField()
    dateSent = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    idEmitter = models.ForeignKey(User, related_name='emitter', on_delete=models.CASCADE)
    idReceiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)

class AdoptionFilters(models.Model):
    class SizeChoices(models.TextChoices):
        PEQUENO = 'Pequeño', 'Pequeño'
        MEDIANO = 'Mediano', 'Mediano'
        GRANDE = 'Grande', 'Grande'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    size = models.CharField(max_length=10, choices=SizeChoices.choices)
    ageMin = models.IntegerField()
    ageMax = models.IntegerField()
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    breed = models.CharField(max_length=30, blank=True, null=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

class UsersProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(blank=True, null=True)
    profilePhotoURL = models.CharField(max_length=254, blank=True, null=True)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=254)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

class Logs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

class PasswordResets(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    resetToken = models.CharField(max_length=100)
    expiration = models.DateTimeField()

class EmailVerifications(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    verificationCode = models.CharField(max_length=100)
    expiration = models.DateTimeField()
    verified = models.BooleanField(default=False)