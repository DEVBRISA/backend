from django.db import models

class Reclamo(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('DNI', 'DNI'),
        ('CE', 'Carnet de extranjería'),
        ('PAS', 'Pasaporte'),
        ('OTRO', 'Otro'),
    ]
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOCUMENTO_CHOICES)
    numero_documento = models.CharField(max_length=20)
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)

    departamento = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    distrito = models.CharField(max_length=100)
    telefono_fijo = models.CharField(max_length=15, blank=True, null=True)
    telefono_celular = models.CharField(max_length=15)
    correo = models.EmailField()

    IDENTIFICACION_CHOICES = [
        ('PRODUCTO', 'Producto'),
        ('SERVICIO', 'Servicio'),
    ]
    identificacion = models.CharField(max_length=20, choices=IDENTIFICACION_CHOICES)
    monto_reclamado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tienda = models.CharField(max_length=100)
    fecha_compra = models.DateField(null=True, blank=True)
    numero_boleta = models.CharField(max_length=50, blank=True, null=True)
    numero_pedido = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.TextField()

    TIPO_RECLAMO_CHOICES = [
        ('RECLAMO', 'Reclamo'),
        ('QUEJA', 'Queja'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_RECLAMO_CHOICES)
    detalle = models.TextField()
    pedido_cliente = models.TextField()

    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombres} {self.apellido_paterno} - {self.tipo}"
