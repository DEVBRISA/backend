from django.db import models
from django.core.validators import RegexValidator, URLValidator, EmailValidator

class Empresa(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    direccion_legal = models.CharField(max_length=255)
    ruc = models.CharField(
        max_length=11,
        unique=True,
        validators=[RegexValidator(r'^\d{11}$', 'El RUC debe contener exactamente 11 dígitos numéricos.')]
    )
    razon_social = models.CharField(max_length=255)
    correo = models.EmailField(unique=True, validators=[EmailValidator('Ingrese un correo electrónico válido.')])
    celular = models.CharField(
        max_length=13,
        validators=[RegexValidator(r'^(\+51)?\d{9}$', 'El número de celular debe contener 9 dígitos o incluir el prefijo +51.')]
    )
    mision = models.TextField()
    vision = models.TextField()
    descripcion = models.TextField()
    slogan = models.CharField(max_length=255, blank=True, null=True)
    valores = models.TextField()
    
    facebook = models.URLField(blank=True, null=True, validators=[URLValidator('Ingrese una URL válida.')])
    tiktok = models.URLField(blank=True, null=True, validators=[URLValidator('Ingrese una URL válida.')])
    instagram = models.URLField(blank=True, null=True, validators=[URLValidator('Ingrese una URL válida.')])
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.nombre
