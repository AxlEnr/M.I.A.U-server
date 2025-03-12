from django.db import models
from django.contrib.auth.hashers import make_password
import uuid
from user.models import User
from pet.models import Pet

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