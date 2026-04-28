from django.db import models
import uuid

class CodeQR(models.Model):
    qr_code_url = models.TextField()
    pdf_url = models.TextField(blank=True, null=True)
    creation_date = models.DateField(auto_now=True)
