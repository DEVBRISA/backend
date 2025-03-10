from django.db import models
from categoria.models import Categoria

class Producto(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField()
    ingrediente = models.TextField(blank=True, null=True)
    detalle = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')

    img1 = models.ImageField(upload_to='productos/', null=False, blank=False)
    img2 = models.ImageField(upload_to='productos/', null=True, blank=True)
    img3 = models.ImageField(upload_to='productos/', null=True, blank=True)
    img4 = models.ImageField(upload_to='productos/', null=True, blank=True)

    modo_uso = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def eliminar_imagen(self, imagen):
        """Elimina la imagen del producto y la establece en `null`."""
        img_attr = getattr(self, imagen)
        if img_attr:
            img_attr.delete(save=False)
            setattr(self, imagen, None)
            self.save()

    def __str__(self):
        return self.nombre
