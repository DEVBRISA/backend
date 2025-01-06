from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, dni, username, nombre=None, apellidos=None, email=None, password=None, **extra_fields):
        if not dni:
            raise ValueError("El DNI es obligatorio")
        if not username:
            raise ValueError("El username es obligatorio")

        user = self.model(
            dni=dni,
            username=username,  # Ahora username es obligatorio
            nombre=nombre,
            apellidos=apellidos,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, dni, username, nombre, apellidos, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(dni, username, nombre, apellidos, email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ('admin', 'Admin'),
        ('default', 'Default'),
    ]

    dni = models.CharField(max_length=8, unique=True, primary_key=True)  
    username = models.CharField(max_length=150, unique=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.URLField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    rol = models.CharField(max_length=10, choices=ROLES, default='default') 

    groups = models.ManyToManyField('auth.Group', related_name='usuario_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='usuario_set', blank=True)

    objects = UsuarioManager()
    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['dni', 'nombre', 'apellidos']  

    def __str__(self):
        return f'{self.nombre} {self.apellidos}'




