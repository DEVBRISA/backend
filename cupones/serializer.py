from rest_framework import serializers
from .models import Cupon
from django.utils import timezone

class CuponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cupon
        fields = '__all__'
        extra_kwargs = {
            "codigo": {"help_text": "Código único del cupón. Ej: BRISAPADRE25"},
            "tipo": {"help_text": "Tipo de cupón: 'porcentaje' o 'monto'"},
            "valor": {"help_text": "Valor del cupón. Ej: 20 para 20% o 50 para S/50"},
            "minimo_compra": {"help_text": "Monto mínimo de compra para aplicar el cupón"},
            "max_descuento": {"help_text": "Descuento máximo permitido (solo aplica si es porcentaje)"},
            "usos_maximos": {"help_text": "Cantidad máxima de usos del cupón (null = ilimitado)"},
        }

    def validate_codigo(self, value):
        if not value.isalnum():
            raise serializers.ValidationError("El código solo puede contener letras y números.")
        if len(value) < 4:
            raise serializers.ValidationError("El código debe tener al menos 4 caracteres.")
        return value.upper()

    def validate_valor(self, value):
        if value <= 0:
            raise serializers.ValidationError("El valor del cupón debe ser mayor a 0.")
        return value

    def validate(self, data):
        tipo = data.get('tipo')
        valor = data.get('valor')
        max_descuento = data.get('max_descuento')
        fecha_inicio = data.get('fecha_inicio', getattr(self.instance, 'fecha_inicio', None))
        fecha_fin = data.get('fecha_fin', getattr(self.instance, 'fecha_fin', None))

        if fecha_inicio and fecha_fin and fecha_fin <= fecha_inicio:
            raise serializers.ValidationError("La fecha de fin debe ser posterior a la fecha de inicio.")

        if tipo == "porcentaje" and valor > 100:
            raise serializers.ValidationError("Un cupón en porcentaje no puede superar el 100%.")
        if tipo == "monto" and max_descuento:
            raise serializers.ValidationError("Un cupón en monto fijo no debe tener 'max_descuento'.")

        return data
