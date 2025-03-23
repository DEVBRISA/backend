from rest_framework import serializers
from productos.models import Producto
from .models import Pack
from productos.serializer import ProductoSerializer

class PackSerializer(serializers.ModelSerializer):
    productos_ids = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(),
        many=True,
        write_only=True,
        source='productos'
    )
    productos = ProductoSerializer(many=True, read_only=True)  # Mostrar productos en la respuesta

    img1 = serializers.ImageField(required=False, allow_null=True)
    img2 = serializers.ImageField(required=False, allow_null=True)
    img3 = serializers.ImageField(required=False, allow_null=True)
    img4 = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Pack
        fields = [
            'sku', 'nombre', 'descripcion', 'productos_ids', 'productos',
            'precio', 'active', 'img1', 'img2', 'img3', 'img4', 
            'fecha_creacion', 'fecha_modificacion'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_modificacion']

    def validate_productos_ids(self, value):
        """Valida que el pack tenga exactamente 3 productos."""
        if len(value) != 3:
            raise serializers.ValidationError("Cada pack debe contener exactamente 3 productos.")
        return value

class PackDeleteImageSerializer(serializers.Serializer):
    """Serializer para eliminar imágenes de un pack usando booleanos."""
    img1 = serializers.BooleanField(required=False, default=False)
    img2 = serializers.BooleanField(required=False, default=False)
    img3 = serializers.BooleanField(required=False, default=False)
    img4 = serializers.BooleanField(required=False, default=False)

    def update(self, instance, validated_data):
        """Elimina las imágenes solo si el booleano es `True`."""
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

class PackDeleteSerializer(serializers.ModelSerializer):
    """Serializer para activar o desactivar un pack"""
    class Meta:
        model = Pack
        fields = ['active']