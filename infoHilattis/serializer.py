from rest_framework import serializers
from infoHilattis.models import infoHilattis

class infoHilattisSerializer(serializers.ModelSerializer):
    class Meta:
        model = infoHilattis
        fields = [
            'id', 'ruc', 'nombre', 'direccion', 'telefono', 'email',
            'mision', 'vision', 'resena', 'fundadora', 'palabras_fundadora',
            'slogan', 'title', 'subtitle'
        ]