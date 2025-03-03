from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models


class UsuarioManager(BaseUserManager):
    def create_user(self, dni, username, nombre, apellidos, email, password=None, **extra_fields):
        if not dni:
            raise ValueError("El DNI es obligatorio")
        if not username:
            raise ValueError("El username es obligatorio")
        if not email:
            raise ValueError("El email es obligatorio")
        if not password:
            raise ValueError("La contraseña es obligatoria")

        user = self.model(
            dni=dni,
            username=username,
            nombre=nombre,
            apellidos=apellidos,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, dni, username, nombre, apellidos, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not password:
            raise ValueError("El superusuario debe tener una contraseña.")

        return self.create_user(dni, username, nombre, apellidos, email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ('admin', 'Admin'),
        ('default', 'Default'),
    ]

    dni = models.CharField(
        max_length=8,
        unique=True,
        primary_key=True,
        validators=[RegexValidator(r'^\d{8}$', 'El DNI debe contener exactamente 8 dígitos numéricos.')]
    )
    username = models.CharField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(r'^[\w.@+-]+$', 'El nombre de usuario solo puede contener letras, números y los caracteres @/./+/-/_')]
    )
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(
    max_length=13,
    null=True,
    blank=True,
        validators=[RegexValidator(
        r'^(\+51)?\d{9}$',
        'El número de teléfono debe ser un celular (9 dígitos) o incluir el prefijo +51 (11 dígitos).'
        )]
    )
    address = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.URLField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    rol = models.CharField(max_length=10, choices=ROLES, default='default')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField('auth.Group', related_name='usuario_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='usuario_set', blank=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['dni', 'nombre', 'apellidos', 'email']

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f'{self.nombre} {self.apellidos}'