from django.db import models
from categoria.models import Categoria
from productos.models import Producto

class Promocion(models.Model):
    TIPO_CHOICES = [
        ('combo', 'Combo'),
        ('descuento', 'Descuento'),
    ]

    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Uno u otro
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)

    cantidad_requerida = models.PositiveIntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    def aplica_a_categoria(self):
        return self.categoria is not None and self.producto is None

    def aplica_a_producto(self):
        return self.producto is not None
