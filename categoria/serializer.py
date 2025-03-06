from rest_framework import serializers
from categoria.models import Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    """ Serializer para la gestión de categorías. """
    
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'imagen', 'fecha_creacion', 'fecha_modificacion']
        read_only_fields = ['fecha_creacion', 'fecha_modificacion']
    
    def update(self, instance, validated_data):
        imagen = validated_data.get('imagen', instance.imagen)
        instance.imagen = imagen 

        return super().update(instance, validated_data)
