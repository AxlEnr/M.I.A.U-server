from django.db import models
from django.conf import settings
from codeQR.models import CodeQR

class Pet(models.Model):
    class SizeChoices(models.TextChoices):
        PEQUENO = 'Pequeno', 'Pequeño'
        MEDIANO = 'Mediano', 'Mediano'
        GRANDE = 'Grande', 'Grande'

    class StatusAdoptions(models.IntegerChoices):
        ADOPTED = 1, 'This pet has family'
        LOST = 0, 'This pet doesnt have family'
        LOOKING = 2, 'This pet is looking for a family'

    name = models.CharField(max_length=30)
    age = models.CharField(max_length=50)
    breed = models.CharField(max_length=30)
    size = models.CharField(max_length=10, choices=SizeChoices.choices)
    petDetails = models.CharField(max_length=254, blank=True, null=True)
    qrId = models.ForeignKey(CodeQR, on_delete=models.CASCADE, null=True)
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    statusAdoption = models.IntegerField(choices=StatusAdoptions.choices, default=StatusAdoptions.LOOKING)