from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, dni, nombre, apellidos, email, password=None, **extra_fields):
        """
        Crear un usuario regular con DNI como clave primaria y contraseña encriptada.
        """
        if not dni:
            raise ValueError("El DNI es obligatorio")
        if not email:
            raise ValueError("El email es obligatorio")
        
        email = self.normalize_email(email)
        user = self.model(dni=dni, nombre=nombre, apellidos=apellidos, email=email, **extra_fields)
        user.set_password(password)  # Encripta la contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, dni, nombre, apellidos, email, password=None, **extra_fields):
        """
        Crear un superusuario con permisos de administrador.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(dni, nombre, apellidos, email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    """
    Modelo personalizado de usuario donde el DNI es la clave primaria.
    """
    dni = models.CharField(max_length=8, unique=True, primary_key=True)  # DNI como clave primaria
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.URLField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    # Añadir related_name para evitar conflictos con el modelo User predeterminado
    groups = models.ManyToManyField('auth.Group', related_name='usuario_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='usuario_set', blank=True)

    objects = UsuarioManager()

    # Campo para iniciar sesión
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['dni', 'nombre', 'apellidos']

    def __str__(self):
        return f'{self.nombre} {self.apellidos}'
