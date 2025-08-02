from rest_framework import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    img1 = serializers.ImageField(write_only=True, required=False)
    img2 = serializers.ImageField(write_only=True, required=False)
    img3 = serializers.ImageField(write_only=True, required=False)
    img4 = serializers.ImageField(write_only=True, required=False)
    sku = serializers.CharField(read_only=True)

    class Meta:
        model = Producto
        fields = [
            'sku', 'nombre', 'descripcion', 'ingrediente', 'detalle', 'precio',
            'img1', 'img2', 'img3', 'img4', 'modo_uso', 'fecha_creacion', 'fecha_modificacion',
            'active', 'categoria', 'pack'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_modificacion']

    def to_representation(self, instance):
        """Mostrar URLs reales en la respuesta"""
        rep = super().to_representation(instance)
        rep['img1'] = instance.img1
        rep['img2'] = instance.img2
        rep['img3'] = instance.img3
        rep['img4'] = instance.img4
        return rep

    def validate_nombre(self, value):
        request = self.context.get('request')
        qs = Producto.objects.filter(nombre__iexact=value)
        if request and request.method in ['PUT', 'PATCH']:
            instance = self.instance
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
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
            has_images = any([
                request.FILES.get('img1'),
                request.FILES.get('img2'),
                request.FILES.get('img3'),
                request.FILES.get('img4')
            ])
        if not has_images:
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
            instance.img1 = ""
        if validated_data.get('img2'):
            instance.img2 = ""
        if validated_data.get('img3'):
            instance.img3 = ""
        if validated_data.get('img4'):
            instance.img4 = ""

        instance.save()
        return instance
    
    
class ProductoPackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['pack']

