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
        
        # Si el producto no es variable, no puede tener variantes
        if not is_variable and variantes:
            raise serializers.ValidationError(
                {"variantes": "Los productos no variables no deben tener variantes."}
            )
        
        # Si el producto es variable, debe tener variantes asignadas
        if is_variable and not variantes:
            raise serializers.ValidationError(
                {"variantes": "Es obligatorio asignar al menos una variante si el producto es variable."}
            )
        
        # Validaciones adicionales para productos variables
        if is_variable:
            if any([data.get('img1'), data.get('img2'), data.get('img3'), data.get('precio')]):
                raise serializers.ValidationError(
                    "Los productos variables no deben tener imágenes adicionales ni precio."
                )
        else:
            if not data.get('imagen_default'):
                raise serializers.ValidationError(
                    {"imagen_default": "La imagen por defecto es obligatoria para productos no variables."}
                )
            if not data.get('precio'):
                raise serializers.ValidationError(
                    {"precio": "El precio es obligatorio para productos no variables."}
                )
        
        return data