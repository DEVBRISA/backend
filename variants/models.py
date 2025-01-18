from django.db import models
from django.core.exceptions import ValidationError

class Variante(models.Model):
    id_variante = models.AutoField(primary_key=True)
    producto = models.ForeignKey(
        'productos.Producto',  # Referencia como string
        on_delete=models.CASCADE,
        related_name='variantes'
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0.0)
    img1 = models.ImageField(upload_to='variantes/', null=True, blank=True)
    img2 = models.ImageField(upload_to='variantes/', null=True, blank=True)
    img3 = models.ImageField(upload_to='variantes/', null=True, blank=True)

    def clean(self):
        """
        Valida que la variante solo pueda asociarse a productos que sean variables.
        """
        if not self.producto.is_variable:
            raise ValidationError("Solo se pueden asociar variantes a productos marcados como variables.")

    def __str__(self):
        return f"{self.producto.nombre} - {self.nombre}"
