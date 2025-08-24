from rest_framework import serializers
from productos.models import Producto
from categoria.models import Categoria
from offer.models import Promocion

class PromocionSerializer(serializers.ModelSerializer):
    producto = serializers.SlugRelatedField(
        queryset=Producto.objects.all(),
        slug_field='sku',
        required=False,
        allow_null=True
    )
    categoria = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Promocion
        fields = '__all__'

    def validate(self, data):
        categoria = data.get('categoria', getattr(self.instance, 'categoria', None))
        producto = data.get('producto', getattr(self.instance, 'producto', None))

        if categoria and producto:
            raise serializers.ValidationError("Una promoción no puede tener categoría y producto al mismo tiempo.")
        if not categoria and not producto:
            raise serializers.ValidationError("Debe asignar la promoción a una categoría o a un producto.")

        fecha_inicio = data.get('fecha_inicio', getattr(self.instance, 'fecha_inicio', None))
        fecha_fin = data.get('fecha_fin', getattr(self.instance, 'fecha_fin', None))

        if fecha_inicio and fecha_fin and fecha_fin <= fecha_inicio:
            raise serializers.ValidationError("La fecha de fin debe ser posterior a la fecha de inicio.")

        return data