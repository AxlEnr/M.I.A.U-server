from django.db import models
from django.contrib.auth.hashers import make_password
import uuid
from user.models import User

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