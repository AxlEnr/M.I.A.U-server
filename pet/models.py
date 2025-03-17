from django.db import models
from django.contrib.auth.hashers import make_password
import uuid
from user.models import User
from codeQR.models import CodeQR
class Pet(models.Model):
    class SizeChoices(models.TextChoices):
        PEQUENO = 'Pequeño', 'Pequeño'
        MEDIANO = 'Mediano', 'Mediano'
        GRANDE = 'Grande', 'Grande'

    class statusAdoptios(models.IntegerChoices):
        adopted = 1, 'This pet has family'
        lost = 0, 'This pet doesnt have family' 

    name = models.CharField(max_length=30)
    age = models.IntegerField()
    breed = models.CharField(max_length=30)
    size = models.CharField(max_length=10, choices=SizeChoices.choices)
    petDetails = models.CharField(max_length=254, blank=True, null=True)
    qrId = models.ForeignKey(CodeQR, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    statusAdoption = models.IntegerField(choices=statusAdoptios.choices, default=0)
