from rest_framework import serializers
from projects.models import Proyecto

class ProyectoSerializer(serializers.ModelSerializer):
    imagen1 = serializers.ImageField(required=False, allow_null=True)
    imagen2 = serializers.ImageField(required=False, allow_null=True)
    imagen3 = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Proyecto
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.titulo = validated_data.get('titulo', instance.titulo)
        instance.fecha_proyecto = validated_data.get('fecha_proyecto', instance.fecha_proyecto)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        
        if 'imagen1' in validated_data:
            instance.imagen1 = validated_data['imagen1']
        if 'imagen2' in validated_data:
            instance.imagen2 = validated_data['imagen2']
        if 'imagen3' in validated_data:
            instance.imagen3 = validated_data['imagen3']
        
        instance.save()
        return instance

    
class ProyectoDeleteImageSerializer(serializers.Serializer):
    imagen1 = serializers.BooleanField(required=False, default=False)
    imagen2 = serializers.BooleanField(required=False, default=False)
    imagen3 = serializers.BooleanField(required=False, default=False)

    def update(self, instance, validated_data):
        if validated_data.get('imagen1', False):
            instance.delete_imagen1()
        if validated_data.get('imagen2', False):
            instance.delete_imagen2()
        if validated_data.get('imagen3', False):
            instance.delete_imagen3()
        return instance

class ProyectoDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = ['id']


