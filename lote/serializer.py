from rest_framework import serializers
from lote.models import Lote
from productos.models import Producto

from rest_framework import serializers
from productos.models import Producto
from lote.models import Lote

class LoteSerializer(serializers.ModelSerializer):
    producto = serializers.SlugRelatedField(
        queryset=Producto.objects.all(),
        slug_field='sku'
    )

    class Meta:
        model = Lote
        fields = ['id', 'producto', 'fecha_fabricacion', 'fecha_vencimiento', 'cantidad', 'fecha_creacion', 'fecha_modificacion']
        read_only_fields = ['fecha_creacion', 'fecha_modificacion']


class LoteCantidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = ['cantidad']