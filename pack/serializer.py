import cloudinary.uploader
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

    img1_file = serializers.ImageField(write_only=True, required=False)
    img2_file = serializers.ImageField(write_only=True, required=False)
    img3_file = serializers.ImageField(write_only=True, required=False)
    img4_file = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Pack
        fields = [
            'sku', 'nombre', 'descripcion', 'productos_ids', 'productos',
            'precio', 'active',
            'img1_file', 'img2_file', 'img3_file', 'img4_file',
            'fecha_creacion', 'fecha_modificacion'
        ]
        read_only_fields = ['sku', 'fecha_creacion', 'fecha_modificacion']

    def validate_productos_ids(self, value):
        if len(value) != 3:
            raise serializers.ValidationError("Cada pack debe contener exactamente 3 productos.")
        return value

    def upload_to_cloudinary(self, file):
        """Sube un archivo a Cloudinary y devuelve la URL segura."""
        result = cloudinary.uploader.upload(file)
        return result.get('secure_url')

    def create(self, validated_data):
        img1_file = validated_data.pop('img1_file', None)
        img2_file = validated_data.pop('img2_file', None)
        img3_file = validated_data.pop('img3_file', None)
        img4_file = validated_data.pop('img4_file', None)

        pack = super().create(validated_data)

        if img1_file:
            pack.img1 = self.upload_to_cloudinary(img1_file)
        if img2_file:
            pack.img2 = self.upload_to_cloudinary(img2_file)
        if img3_file:
            pack.img3 = self.upload_to_cloudinary(img3_file)
        if img4_file:
            pack.img4 = self.upload_to_cloudinary(img4_file)

        pack.save()
        return pack

    def update(self, instance, validated_data):
        img1_file = validated_data.pop('img1_file', None)
        img2_file = validated_data.pop('img2_file', None)
        img3_file = validated_data.pop('img3_file', None)
        img4_file = validated_data.pop('img4_file', None)

        instance = super().update(instance, validated_data)

        if img1_file:
            instance.img1 = self.upload_to_cloudinary(img1_file)
        if img2_file:
            instance.img2 = self.upload_to_cloudinary(img2_file)
        if img3_file:
            instance.img3 = self.upload_to_cloudinary(img3_file)
        if img4_file:
            instance.img4 = self.upload_to_cloudinary(img4_file)

        instance.save()
        return instance


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
