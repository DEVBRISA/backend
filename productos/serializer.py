from rest_framework import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [
            'sku', 'nombre', 'descripcion', 'ingrediente', 'detalle', 'precio',
            'img1', 'img2', 'img3', 'img4', 'modo_uso', 'fecha_creacion', 'fecha_modificacion',
            'active', 'categoria', 'pack'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_modificacion']

    def validate_nombre(self, value):
        """Valida que el nombre no esté duplicado."""
        if Producto.objects.filter(nombre__iexact=value).exists():
            raise serializers.ValidationError("Ya existe un producto con este nombre.")
        return value

    def validate_precio(self, value):
        """Valida que el precio sea mayor a 0."""
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser un valor positivo.")
        return value

    def validate(self, data):
        request = self.context.get('request')
        if request and request.method == 'POST':
         if not any([data.get('img1'), data.get('img2'), data.get('img3'), data.get('img4')]):
            raise serializers.ValidationError({"error": "Se requiere al menos una imagen del producto."})
        return data


class ProductoDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['active']

    def update(self, instance, validated_data):
        """Método que actualiza el campo `active` del producto."""
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance


class ProductoDeleteImageSerializer(serializers.Serializer):
    img1 = serializers.BooleanField(required=False, default=False)
    img2 = serializers.BooleanField(required=False, default=False)
    img3 = serializers.BooleanField(required=False, default=False)
    img4 = serializers.BooleanField(required=False, default=False)

    def update(self, instance, validated_data):
        if validated_data.get('img1'):
            instance.img1.delete(save=False)
            instance.img1 = None
        if validated_data.get('img2'):
            instance.img2.delete(save=False)
            instance.img2 = None
        if validated_data.get('img3'):
            instance.img3.delete(save=False)
            instance.img3 = None
        if validated_data.get('img4'):
            instance.img4.delete(save=False)
            instance.img4 = None

        instance.save()
        return instance
    
class ProductoPackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['pack']

