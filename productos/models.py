from django.db import models
from categoria.models import Categoria

class Producto(models.Model):
    sku = models.CharField(max_length=50, unique=True, blank=True)
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField()
    ingrediente = models.TextField(blank=True, null=True)
    detalle = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    pack = models.BooleanField(default=False)

    img1 = models.CharField(max_length=500, blank=True, null=True)
    img2 = models.CharField(max_length=500, blank=True, null=True)
    img3 = models.CharField(max_length=500, blank=True, null=True)
    img4 = models.CharField(max_length=500, blank=True, null=True)

    modo_uso = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.sku: 
            last_product = Producto.objects.order_by('-id').first()
            next_id = (last_product.id + 1) if last_product else 1
            self.sku = f'BRISA-{next_id}'
        super().save(*args, **kwargs)

    def eliminar_imagen(self, imagen):
        """Elimina la URL de la imagen del producto y la establece en `null`."""
        if hasattr(self, imagen):
            setattr(self, imagen, None)
        self.save()

    def __str__(self):
        return self.nombre 
