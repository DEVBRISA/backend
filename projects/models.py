from django.db import models

class Proyecto(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    fecha_proyecto = models.DateField()
    fecha_create = models.DateTimeField(auto_now_add=True)
    fecha_modification = models.DateTimeField(auto_now=True)
    descripcion = models.TextField()
    imagen1 = models.ImageField(upload_to='projects/', null=True, blank=True)
    imagen2 = models.ImageField(upload_to='projects/', null=True, blank=True)
    imagen3 = models.ImageField(upload_to='projects/', null=True, blank=True)

    def __str__(self):
        return self.titulo
    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def delete_imagen1(self):
        """Método para eliminar imagen1 sin borrar el proyecto"""
        if self.imagen1:
            self.imagen1.delete(save=False)
            self.imagen1 = None
            self.save()

    def delete_imagen2(self):
        """Método para eliminar imagen2 sin borrar el proyecto"""
        if self.imagen2:
            self.imagen2.delete(save=False)
            self.imagen2 = None
            self.save()

    def delete_imagen3(self):
        """Método para eliminar imagen3 sin borrar el proyecto"""
        if self.imagen3:
            self.imagen3.delete(save=False)
            self.imagen3 = None
            self.save()
