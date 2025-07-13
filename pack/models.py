from django.db import models
from categoria.models import Categoria
from productos.models import Producto

class Pack(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField()
    productos = models.ManyToManyField(Producto, related_name='packs') 
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    img1 = models.CharField(max_length=500, blank=True, null=True)
    img2 = models.CharField(max_length=500, blank=True, null=True)
    img3 = models.CharField(max_length=500, blank=True, null=True)
    img4 = models.CharField(max_length=500, blank=True, null=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def eliminar_imagen(self, imagen):
        """Elimina la imagen del pack (vacía el string del campo)."""
        if hasattr(self, imagen):
            setattr(self, imagen, "")
        self.save()


    def __str__(self):
        return self.nombre

