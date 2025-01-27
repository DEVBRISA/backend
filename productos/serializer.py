from rest_framework import serializers
from .models import Producto
from variants.models import Variante

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

    def validate(self, data):
        if not data.get('imagen_default'):
            raise serializers.ValidationError(
                {"imagen_default": "La imagen por defecto es obligatoria."}
            )
        if not data.get('precio'):
            raise serializers.ValidationError(
                {"precio": "El precio es obligatorio."}
            )
        if not data.get('descripcion'):
            raise serializers.ValidationError(
                {"descripcion": "La descripción es obligatoria."}
            )
        return data

    def create(self, validated_data):
        return Producto.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class ProductoDeleteImageSerializer(serializers.Serializer):
    imagen1 = serializers.BooleanField(required=False, default=False)
    imagen2 = serializers.BooleanField(required=False, default=False)
    imagen3 = serializers.BooleanField(required=False, default=False)

    def update(self, instance, validated_data):
        if validated_data.get('imagen1', False):
            instance.delete_img1()
        if validated_data.get('imagen2', False):
            instance.delete_img2()
        if validated_data.get('imagen3', False):
            instance.delete_img3()
        return instance