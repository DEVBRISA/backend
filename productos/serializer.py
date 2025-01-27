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
        variantes = self.initial_data.get('variantes', [])

        # Si el producto no es variable, no puede tener variantes
        if not is_variable and variantes:
            raise serializers.ValidationError(
                {"variantes": "Los productos no variables no deben tener variantes."}
            )

        # Validaciones adicionales para productos variables
        if is_variable:
            if any([data.get('img1'), data.get('img2'), data.get('img3'), data.get('precio')]):
                raise serializers.ValidationError(
                    "Los productos variables no deben tener imágenes adicionales ni precio."
                )
        else:
            if 'imagen_default' in data and not data.get('imagen_default'):
                raise serializers.ValidationError(
                    {"imagen_default": "La imagen por defecto es obligatoria para productos no variables."}
                )
            if not data.get('precio'):
                raise serializers.ValidationError(
                    {"precio": "El precio es obligatorio para productos no variables."}
                )

        return data

    def create(self, validated_data):
        """
        Permitir la creación de un producto variable sin variantes.
        """
        variantes = validated_data.pop('variantes', None)
        producto = Producto.objects.create(**validated_data)
        return producto

    def update(self, instance, validated_data):
        # Si imagen_default está vacía, mantener la existente
        if 'imagen_default' in validated_data and validated_data['imagen_default'] == "":
            validated_data.pop('imagen_default')

        # Asignar valores actualizados
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    
class ProductoDeleteImageSerializer(serializers.Serializer):
    imagen1 = serializers.BooleanField(required=False, default=False)
    imagen2 = serializers.BooleanField(required=False, default=False)
    imagen3 = serializers.BooleanField(required=False, default=False)

    def update(self, instance, validated_data):
        if validated_data.get('img1', False):
            instance.delete_img1()
        if validated_data.get('img2', False):
            instance.delete_img2()
        if validated_data.get('img', False):
            instance.delete_img3()
        return instance
