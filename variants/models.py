from django.db import models
from productos.models import Producto

class Variante(models.Model):
    id_variante = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='variantes')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    img1 = models.ImageField(upload_to='variantes/', null=False, blank=False)
    img2 = models.ImageField(upload_to='variantes/', null=False, blank=False)
    img3 = models.ImageField(upload_to='variantes/', null=False, blank=False)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return f"{self.producto.nombre} - {self.nombre}"