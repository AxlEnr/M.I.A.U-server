from django.db import models
from django.contrib.auth.hashers import make_password
import uuid
from user.models import User

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

