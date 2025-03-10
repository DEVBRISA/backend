from rest_framework import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['sku', 'nombre', 'descripcion', 'ingrediente', 'detalle', 'precio', 'cantidad', 'fecha_fabricacion', 'fecha_vencimiento',
                  'img1', 'img2', 'img3', 'img4', 'modo_uso', 'fecha_creacion', 'fecha_modificacion', 'active', 'visible']
        read_only_fields = ['fecha_creacion', 'fecha_modificacion']
    
    def validate_nombre(self, value):
        if Producto.objects.filter(nombre__iexact=value).exists():
            raise serializers.ValidationError("Ya existe un producto con este nombre.")
        return value
    
    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser un valor positivo.")
        return value
    
    def validate(self, data):
        if not data.get('img1'):
            raise serializers.ValidationError({"img1": "Se requiere al menos una imagen."})
        return data
    
    def update(self, instance, validated_data):
        imagen = validated_data.get('imagen', instance.imagen)
        instance.imagen = imagen 
        return super().update(instance, validated_data)
    
class ToggleProductoVisibilitySerializer(serializers.Serializer):
    visible = serializers.BooleanField()

class ProductoDeleteSerializer(serializers.Serializer):
    active = serializers.BooleanField()

class ProductoDeleteImageSerializer(serializers.Serializer):
    img1 = serializers.BooleanField(required=False, default=False)
    img2 = serializers.BooleanField(required=False, default=False)
    img3 = serializers.BooleanField(required=False, default=False)
    img4 = serializers.BooleanField(required=False, default=False)

    def update(self, instance, validated_data):
        if validated_data.get('img1', False):
            instance.delete_img1()
        if validated_data.get('img2', False):
            instance.delete_img2()
        if validated_data.get('img3', False):
            instance.delete_img3()
        if validated_data.get('img4', False):
                instance.delete_img4()
        return instance

