from django.db import models

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    celular = models.CharField(max_length=15)
    mensaje = models.TextField()
    archivo = models.FileField(upload_to='contactos/', null=True, blank=True)
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.correo}"
