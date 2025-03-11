from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
class User(models.Model):
    # Options for role field
    class Roles(models.TextChoices):
        ADMIN = "admin", "Administrator"
        USER = "user", "User"

    class StatusChoices(models.IntegerChoices):  # Usar IntegerChoices en vez de TextChoices
        ACTIVATED = 1, "The account is active"
        DEACTIVATED = 2, "The account is not active"



    # Other Fields
    name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    address = models.CharField(max_length=254)
    created_date = models.DateField(verbose_name='Date when the account was registered', auto_now_add=True)   
    status = models.IntegerField(choices=StatusChoices.choices, default=StatusChoices.ACTIVATED)
    role = models.CharField(choices=Roles.choices, max_length=20, default=Roles.USER)

    # Function to encrypt the password
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
