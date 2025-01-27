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

    def delete_img1(self):
        if self.img1:
            self.img1.delete(save=False)
            self.img1 = None
            self.save()

    def delete_img2(self):
        if self.img2:
            self.img2.delete(save=False)
            self.img2 = None
            self.save()

    def delete_img3(self):
        if self.img3:
            self.img3.delete(save=False)
            self.img3 = None
            self.save()

    def __str__(self):
        return f"{self.producto.nombre} - {self.nombre}"
