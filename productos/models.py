from django.db import models

class Producto(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    ingrediente = models.TextField(blank=True, null=True)
    detalle = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField(default=0)
    fecha_fabricacion = models.DateField()
    fecha_vencimiento = models.DateField()
    
    img1 = models.ImageField(upload_to='productos/', null=False, blank=False)
    img2 = models.ImageField(upload_to='productos/', null=True, blank=True)
    img3 = models.ImageField(upload_to='productos/', null=True, blank=True)
    img4 = models.ImageField(upload_to='productos/', null=True, blank=True)
    
    modo_uso = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        # Reemplazar imágenes antiguas por nuevas
        if self.pk:
            old_instance = Producto.objects.get(pk=self.pk)
            for field in ['img1', 'img2', 'img3', 'img4']:
                old_file = getattr(old_instance, field)
                new_file = getattr(self, field)
                if old_file and old_file != new_file:
                    old_file.delete(save=False)
        super().save(*args, **kwargs)
