from django.db import models
from django.core.exceptions import ValidationError
from productos.models import Producto

class Lote(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='lotes')
    fecha_fabricacion = models.DateField()
    fecha_vencimiento = models.DateField()
    cantidad = models.PositiveIntegerField()

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.fecha_vencimiento <= self.fecha_fabricacion:
            raise ValidationError({'fecha_vencimiento': 'La fecha de vencimiento debe ser mayor que la de fabricación.'})
        if self.cantidad < 0:
            raise ValidationError({'cantidad': 'La cantidad no puede ser negativa.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Lote de {self.producto.nombre} - {self.fecha_fabricacion}"
