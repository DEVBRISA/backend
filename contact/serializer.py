from rest_framework import serializers
from .models import Contacto

class ContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = ['id', 'nombre', 'correo', 'celular', 'mensaje', 'archivo', 'fecha_envio']
        read_only_fields = ['fecha_envio']
