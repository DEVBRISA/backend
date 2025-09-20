from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Cupon(models.Model):
    TIPO_CHOICES = [
        ('porcentaje', 'Porcentaje'),
        ('monto', 'Monto fijo'),
    ]

    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    minimo_compra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    max_descuento = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    usos_maximos = models.PositiveIntegerField(null=True, blank=True)
    usos_actuales = models.PositiveIntegerField(default=0)

    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()

    is_active = models.BooleanField(default=True)  
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.codigo}"

    def clean(self):
        if self.fecha_fin <= self.fecha_inicio:
            raise ValidationError({'fecha_fin': 'La fecha de fin debe ser posterior a la fecha de inicio.'})

    def disponible(self):
        ahora = timezone.now()
        if not self.is_active:
            return False
        if self.fecha_inicio > ahora or self.fecha_fin < ahora:
            return False
        if self.usos_maximos and self.usos_actuales >= self.usos_maximos:
            return False
        return True

    def aplicar_descuento(self, monto_compra):
        if self.minimo_compra and monto_compra < self.minimo_compra:
            return 0

        if self.tipo == 'porcentaje':
            descuento = (monto_compra * self.valor / 100)
            if self.max_descuento:
                descuento = min(descuento, self.max_descuento)
        else:
            descuento = self.valor

        return max(descuento, 0)

