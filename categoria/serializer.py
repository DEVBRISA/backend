from rest_framework import serializers
from categoria.models import Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    imagen_file = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Categoria
        fields = [
            'id', 'nombre', 'descripcion', 'imagen', 'imagen_file',
            'fecha_creacion', 'fecha_modificacion', 'active', 'visible'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_modificacion', 'imagen']  # imagen solo lectura

    def create(self, validated_data):
        validated_data.pop('imagen_file', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('imagen_file', None)
        return super().update(instance, validated_data)

    def validate_nombre(self, value):
        request = self.context.get('request')
        qs = Categoria.objects.filter(nombre__iexact=value)
        if request and request.method in ['PUT', 'PATCH'] and self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Ya existe una categoría con este nombre.")
        return value


class CategoriaDeleteSerializer(serializers.Serializer):
    active = serializers.BooleanField()


class ToggleCategoriaVisibilitySerializer(serializers.Serializer):
    visible = serializers.BooleanField()


