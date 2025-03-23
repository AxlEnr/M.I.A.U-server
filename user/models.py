from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password

# 🔹 Administrador del modelo User
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)

# 🔹 Modelo de usuario personalizado
class User(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices):
        ADMIN = "admin", "Administrator"
        USER = "user", "User"

    class StatusChoices(models.IntegerChoices):
        ACTIVATED = 1, "The account is active"
        DEACTIVATED = 2, "The account is not active"

    # 🔹 Campos del usuario
    name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    address = models.CharField(max_length=254)
    created_date = models.DateField(auto_now_add=True)   
    status = models.IntegerField(choices=StatusChoices.choices, default=StatusChoices.ACTIVATED)
    role = models.CharField(choices=Roles.choices, max_length=20, default=Roles.USER)
    
    # 🔹 Campos necesarios para Django
    is_active = models.BooleanField(default=True)  # Usuario activo/inactivo
    is_staff = models.BooleanField(default=False)  # Permiso para acceder al admin
    is_superuser = models.BooleanField(default=False)  # Superusuario

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "first_name", "age", "phone_number", "address"]

    objects = UserManager()

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

# 🔹 Modelo de perfil de usuario
class UsersProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')  # related_name único
    profilePhoto = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=254, blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.name}"