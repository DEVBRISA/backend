from rest_framework import serializers
from .models import Promocion

class PromocionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocion
        fields = '__all__'

    def validate(self, data):
        if data.get('categoria') and data.get('producto'):
            raise serializers.ValidationError("Una promoción no puede tener categoría y producto al mismo tiempo.")
        if not data.get('categoria') and not data.get('producto'):
            raise serializers.ValidationError("Debe asignar la promoción a una categoría o a un producto.")
        return data
