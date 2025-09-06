from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class ClienteManager(BaseUserManager):
    def create_user(self, email, nombre, apellido, tipo_documento, numero_documento, password=None):
        if not email:
            raise ValueError("El cliente debe tener un email")
        email = self.normalize_email(email)
        cliente = self.model(
            email=email,
            nombre=nombre,
            apellido=apellido,
            tipo_documento=tipo_documento,
            numero_documento=numero_documento
        )
        cliente.set_password(password)
        cliente.save(using=self._db)
        return cliente

    def create_superuser(self, email, nombre, apellido, tipo_documento, numero_documento, password=None):
        cliente = self.create_user(email, nombre, apellido, tipo_documento, numero_documento, password)
        cliente.is_admin = True
        cliente.save(using=self._db)
        return cliente


class Cliente(AbstractBaseUser):
    TIPO_DOCUMENTO_CHOICES = [
        ("DNI", "DNI"),
        ("CE", "Carnet de Extranjería"),
        ("PAS", "Pasaporte"),
    ]

    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    tipo_documento = models.CharField(max_length=3, choices=TIPO_DOCUMENTO_CHOICES, default="DNI")
    numero_documento = models.CharField(max_length=12, unique=True)

    telefono = models.CharField(max_length=15, null=True, blank=True)
    password = models.CharField(max_length=128)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombre", "apellido", "tipo_documento", "numero_documento"]

    objects = ClienteManager()

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.email}"

    @property
    def is_staff(self):
        return self.is_admin


class OTP(models.Model):
    cliente = models.ForeignKey("Cliente", on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    code = models.CharField(max_length=6)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(minutes=5)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"OTP {self.code} para {self.email}"
