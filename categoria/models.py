from django.db import models

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    imagen = models.ImageField(upload_to='categorias/', null=True, blank=True)
    visible = models.BooleanField(default=False)  # Campo añadido

    def __str__(self):
        return self.nombre
