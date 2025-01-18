from rest_framework import serializers
from .models import Producto
from variants.models import Variante

class ProductoSerializer(serializers.ModelSerializer):
    variantes = serializers.PrimaryKeyRelatedField(queryset=Variante.objects.all(), many=True, required=False)

    class Meta:
        model = Producto
        fields = '__all__'

    def validate(self, data):
        is_variable = data.get('is_variable', False)
        variantes = data.get('variantes', [])
        
        if not is_variable:
            if variantes:
                raise serializers.ValidationError(
                    {"variantes": "Los productos no variables no deben tener variantes."}
                )
            if not data.get('imagen_default'):
                raise serializers.ValidationError(
                    {"imagen_default": "La imagen por defecto es obligatoria para productos no variables."}
                )
            if not data.get('precio'):
                raise serializers.ValidationError(
                    {"precio": "El precio es obligatorio para productos no variables."}
                )
        
        if is_variable:
            if not variantes:
                raise serializers.ValidationError(
                    {"variantes": "Es obligatorio asignar al menos una variante si el producto es variable."}
                )
            for campo in ['img1', 'img2', 'img3', 'precio']:
                if data.get(campo):
                    raise serializers.ValidationError(
                        {campo: f"El campo {campo} no está permitido para productos variables."}
                    )

        return data
