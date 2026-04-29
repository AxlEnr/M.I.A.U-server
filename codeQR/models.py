from django.db import models
import uuid
from pet.models import Pet

class CodeQR(models.Model):
    qr_code_url = models.TextField()
    qr_image = models.ImageField(upload_to='qrs/', null=True, blank=True)
    pet = models.OneToOneField(Pet, on_delete=models.CASCADE, related_name='qr', default=1)
    creation_date = models.DateField(auto_now=True)