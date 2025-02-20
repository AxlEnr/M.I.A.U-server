from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
class User(models.Model):
    #Options to role field
    class Roles(models.TextChoices):
        admin = "admin", "adminstrator"
        user = "user", "user"

    #role field
    roles = models.CharField(
        max_length=10,
        choices=Roles.choices #Put the options in roles
    )

    #Other Fields
    name = models.CharField(max_length=30)
    firstName = models.CharField(max_length=30)
    age = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=128)
    phoneNumber = models.CharField(max_length=12, null=True)
    address = models.CharField(max_length=254)
    createdDate = models.DateField(verbose_name='Date when the account was registered', auto_now_add=True)   

    #Function to encrypt the password
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
