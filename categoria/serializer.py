from rest_framework import serializers
from categoria.models import Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    """ Serializer para la gestión de categorías. """
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'imagen', 'fecha_creacion', 'fecha_modificacion', 'active', 'visible']
        read_only_fields = ['fecha_creacion', 'fecha_modificacion']
    
    def validate_nombre(self, value):
        """ Validación para evitar nombres duplicados (sin distinción de mayúsculas/minúsculas). """
        if Categoria.objects.filter(nombre__iexact=value).exists():
            raise serializers.ValidationError("Ya existe una categoría con este nombre.")
        return value
    
    def update(self, instance, validated_data):
        imagen = validated_data.get('imagen', instance.imagen)
        instance.imagen = imagen 
        return super().update(instance, validated_data)
    
class ToggleCategoriaVisibilitySerializer(serializers.Serializer):
        visible = serializers.BooleanField()

class CategoriaDeleteSerializer(serializers.Serializer):
    active = serializers.BooleanField()