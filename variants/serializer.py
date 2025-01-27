from rest_framework import serializers
from .models import Variante
from productos.models import Producto

class VarianteSerializer(serializers.ModelSerializer):
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all(), required=False) 

    class Meta:
        model = Variante
        fields = '__all__'

    def validate(self, data):
        producto = data.get('producto', self.instance.producto if self.instance else None)
        if not producto:
            raise serializers.ValidationError({"producto": "El producto es obligatorio."})
        return data

    def validate_for_create(self, data):
        if not data.get('img1'):
            raise serializers.ValidationError(
                {"img1": "La imagen principal (img1) es obligatoria para las variantes"}
            )
        if not data.get('nombre'):
            raise serializers.ValidationError(
                {"nombre": "El nombre es obligatorio para las variantes"}
            )
        if data.get('precio') is None or data['precio'] < 0:
            raise serializers.ValidationError(
                {"precio": "El precio es obligatorio y debe ser mayor o igual a 0"}
            )
        return data

    def validate_for_update(self, data):
        if 'img1' in data and not data['img1']:
            raise serializers.ValidationError(
                {"img1": "La imagen principal (img1) no puede estar vacía"}
            )
        if 'nombre' in data and not data['nombre']:
            raise serializers.ValidationError(
                {"nombre": "El nombre no puede estar vacío"}
            )
        if 'precio' in data and (data['precio'] is None or data['precio'] < 0):
            raise serializers.ValidationError(
                {"precio": "El precio debe ser mayor o igual a 0"}
            )
        return data

    def create(self, validated_data):
        self.validate_for_create(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self.validate_for_update(validated_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    
class VarianteDeleteImageSerializer(serializers.ModelSerializer):
    imagen1 = serializers.BooleanField(required=False, default=False)
    imagen2 = serializers.BooleanField(required=False, default=False)
    imagen3 = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = Variante
        fields = ['imagen1', 'imagen2', 'imagen3']

    def update(self, instance, validated_data):
        if validated_data.get('imagen1', False):
            instance.delete_img1()
        if validated_data.get('imagen2', False):
            instance.delete_img2()
        if validated_data.get('imagen3', False):
            instance.delete_img3()
        return instance
