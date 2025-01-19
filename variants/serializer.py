from rest_framework import serializers
from .models import Variante
from productos.models import Producto

class VarianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variante
        fields = '__all__'

    def validate(self, data):
        # Validar que el producto asociado sea variable
        producto = data.get('producto')
        if not producto.is_variable:
            raise serializers.ValidationError(
                {"producto": "Solo se pueden asociar variantes a productos marcados como variables."}
            )
        
        # Validar que img1 sea obligatorio
        if not data.get('img1'):
            raise serializers.ValidationError(
                {"img1": "La imagen principal (img1) es obligatoria para las variantes."}
            )
        
        # Validar que nombre sea obligatorio
        if not data.get('nombre'):
            raise serializers.ValidationError(
                {"nombre": "El nombre es obligatorio para las variantes."}
            )

        # Validar que precio sea obligatorio y mayor o igual a 0
        if data.get('precio') is None or data['precio'] < 0:
            raise serializers.ValidationError(
                {"precio": "El precio es obligatorio y debe ser mayor o igual a 0."}
            )
        
        return data
