from rest_framework import serializers
from usuarios.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['dni', 'username', 'nombre', 'apellidos', 'email', 'phone', 'address']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['dni', 'username', 'nombre', 'apellidos', 'email', 'phone', 'address', 'password']

    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True) 
    password = serializers.CharField(required=True, write_only=True)

