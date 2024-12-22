from django.db import models

class infoHilattis(models.Model):
    ruc = models.CharField(max_length=11, unique=True)  # RUC (registro único de contribuyente)
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    mision = models.TextField(null=True, blank=True)
    vision = models.TextField(null=True, blank=True)
    resena = models.TextField(null=True, blank=True)  # Reseña de la empresa
    fundadora = models.CharField(max_length=255, null=True, blank=True)  # Fundadora de la empresa
    palabras_fundadora = models.TextField(null=True, blank=True)  # Mensaje o palabras de la fundadora
    slogan = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    subtitle = models.CharField(max_length=255, null=True, blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

