from django.db import models
from categoria.models import Categoria
from productos.models import Producto

class Pack(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField()
    productos = models.ManyToManyField(Producto, related_name='packs') 
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    img1 = models.ImageField(upload_to='packs/', null=False, blank=False)
    img2 = models.ImageField(upload_to='packs/', null=True, blank=True)
    img3 = models.ImageField(upload_to='packs/', null=True, blank=True)
    img4 = models.ImageField(upload_to='packs/', null=True, blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def eliminar_imagen(self, imagen):
        """Elimina la imagen del pack y la establece en `null`."""
        img_attr = getattr(self, imagen)
        if img_attr:
            img_attr.delete(save=False)
            setattr(self, imagen, None)
            self.save()

    def __str__(self):
        return self.nombre

