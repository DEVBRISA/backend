from django.db import models

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    id_categoria = models.ForeignKey('categoria.categoria', on_delete=models.CASCADE, related_name='productos')
    imagen_default = models.ImageField(upload_to='productos/', null=True, blank=False)
    img1 = models.ImageField(upload_to='productos/', null=True, blank=True)
    img2 = models.ImageField(upload_to='productos/', null=True, blank=True)
    img3 = models.ImageField(upload_to='productos/', null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_variable = models.BooleanField(default=False)
    estatus = models.CharField(
        max_length=10,
        choices=[('DISPONIBLE', 'Disponible'), ('AGOTADO', 'Agotado')],
        default='AGOTADO'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
