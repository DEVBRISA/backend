from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from usuarios.models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    """ Serializer para leer datos de usuario (oculta contraseña). """
    
    class Meta:
        model = Usuario
        fields = ['dni', 'username', 'nombre', 'apellidos', 'email', 'phone', 'address', 'is_active', 'rol']
        read_only_fields = ['is_active']


class RegisterSerializer(serializers.ModelSerializer):
    """ Serializer para registrar nuevos usuarios. """
    
    class Meta:
        model = Usuario
        fields = ['dni', 'username', 'nombre', 'apellidos', 'email', 'phone', 'address', 'password', 'rol']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_username(self, value):
        """ Validación de unicidad para username. """
        if Usuario.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está en uso.")
        return value

    def validate_email(self, value):
        """ Validación de unicidad para email. """
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo electrónico ya está registrado.")
        return value

    def create(self, validated_data):
        """ Crea un usuario con la contraseña encriptada. """
        validated_data['is_active'] = True
        validated_data['password'] = make_password(validated_data['password'])
        return Usuario.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    """ Serializer para el login de usuarios. """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True, trim_whitespace=False)


class UsuarioChangeStateSerializer(serializers.ModelSerializer):
    """ Serializer para cambiar el estado activo del usuario. """
    
    class Meta:
        model = Usuario
        fields = ['is_active']

