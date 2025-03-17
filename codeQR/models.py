from django.db import models
import uuid

# Create your models here.
class CodeQR(models.Model):
    # Options for role field
    qr_code_url = models.URLField(max_length=254)
    pdf_url = models.URLField(max_length=254)
    creation_date = models.DateField(auto_now=True)
