from rest_framework import serializers
from empresa.models import Empresa

class EmpresaSerializer(serializers.ModelSerializer):
    """ Serializer para la información de la empresa. """
    
    class Meta:
        model = Empresa
        fields = ['id', 'nombre', 'direccion_legal', 'ruc', 'razon_social', 'correo', 'celular', 'mision', 'vision', 'descripcion', 'slogan', 'valores', 'facebook', 'tiktok', 'instagram', 'fecha_creacion', 'fecha_modificacion']
