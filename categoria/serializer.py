from rest_framework import serializers
from .models import Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__' 

    def update(self, instance, validated_data):
        imagen = validated_data.get('imagen', instance.imagen)
        instance.imagen = imagen 

        return super().update(instance, validated_data)

