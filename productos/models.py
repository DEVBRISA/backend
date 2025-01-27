from django.db import models
from django.core.exceptions import ValidationError

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    id_categoria = models.ForeignKey(
        'categoria.categoria', 
        on_delete=models.CASCADE, 
        related_name='productos'
    )
    imagen_default = models.ImageField(upload_to='productos/', null=True, blank=True)
    img1 = models.ImageField(upload_to='productos/', null=True, blank=True)
    img2 = models.ImageField(upload_to='productos/', null=True, blank=True)
    img3 = models.ImageField(upload_to='productos/', null=True, blank=True)
    is_variable = models.BooleanField(default=False)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.0)
    descripcion = models.TextField(null=True, blank=True)
    estatus = models.CharField(
        max_length=10,
        choices=[('DISPONIBLE', 'Disponible'), ('AGOTADO', 'Agotado')],
        default='AGOTADO'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.is_variable:
            if self.precio or self.descripcion:
                raise ValidationError("Los productos variables no deben tener precio ni descripción.")
        else:
            from variants.models import Variante  # Import dentro del método
            if Variante.objects.filter(producto=self).exists():
                raise ValidationError("Los productos no variables no pueden tener variantes asociadas.")


    def delete_img1(self):
        """Método para eliminar img1 sin borrar el producto"""
        if self.img1:
            self.img1.delete(save=False)
            self.img1 = None
            self.save()

    def delete_img2(self):
        """Método para eliminar img2 sin borrar el producto"""
        if self.img2:
            self.img2.delete(save=False)
            self.img2 = None
            self.save()

    def delete_img3(self):
        """Método para eliminar img3 sin borrar el producto"""
        if self.img3:
            self.img3.delete(save=False)
            self.img3 = None
            self.save()

    def __str__(self):
        return self.nombre
