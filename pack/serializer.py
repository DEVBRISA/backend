from rest_framework import serializers
from productos.models import Producto
from .models import Pack
from productos.serializer import ProductoSerializer

class PackSerializer(serializers.ModelSerializer):
    sku = serializers.CharField(read_only=True)
    productos_ids = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(),
        many=True,
        write_only=True,
        source='productos'
    )
    productos = ProductoSerializer(many=True, read_only=True)

    img1 = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    img2 = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    img3 = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    img4 = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Pack
        fields = [
            'sku', 'nombre', 'descripcion', 'productos_ids', 'productos',
            'precio', 'active', 'img1', 'img2', 'img3', 'img4', 
            'fecha_creacion', 'fecha_modificacion'
        ]
        read_only_fields = ['sku', 'fecha_creacion', 'fecha_modificacion']

    def validate_productos_ids(self, value):
        if len(value) != 3:
            raise serializers.ValidationError("Cada pack debe contener exactamente 3 productos.")
        return value

class PackDeleteImageSerializer(serializers.Serializer):
    img1 = serializers.BooleanField(required=False, default=False)
    img2 = serializers.BooleanField(required=False, default=False)
    img3 = serializers.BooleanField(required=False, default=False)
    img4 = serializers.BooleanField(required=False, default=False)

    def update(self, instance, validated_data):
        """Elimina las imágenes (pone cadena vacía) si el booleano es `True`."""
        if validated_data.get('img1'):
            instance.img1 = ""
        if validated_data.get('img2'):
            instance.img2 = ""
        if validated_data.get('img3'):
            instance.img3 = ""
        if validated_data.get('img4'):
            instance.img4 = ""

        instance.save()
        return instance

class PackDeleteSerializer(serializers.ModelSerializer):
    """Serializer para activar o desactivar un pack"""
    class Meta:
        model = Pack
        fields = ['active']