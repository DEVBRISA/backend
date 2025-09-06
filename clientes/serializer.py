from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import Cliente

from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import Cliente


class RegistroClienteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    telefono = serializers.CharField(
        required=False,
        validators=[RegexValidator(r'^\+?\d{7,15}$', "Debe ser un número de teléfono válido")]
    )

    class Meta:
        model = Cliente
        fields = [
            "email",
            "nombre",
            "apellido",
            "tipo_documento",
            "numero_documento",
            "telefono",
            "password",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        cliente = Cliente(**validated_data)
        cliente.set_password(password)
        cliente.save()
        return cliente

    def validate_tipo_documento(self, value):
        allowed = [choice[0] for choice in Cliente.TIPO_DOCUMENTO_CHOICES]
        if value not in allowed:
            raise serializers.ValidationError("Tipo de documento inválido, debe ser 'DNI', 'CE' o 'PAS'.")
        return value

    def validate(self, data):
        tipo = data.get("tipo_documento")
        numero = data.get("numero_documento")

        if tipo == "DNI":
            if not numero.isdigit() or len(numero) != 8:
                raise serializers.ValidationError({"numero_documento": "El DNI debe tener exactamente 8 dígitos."})
        elif tipo == "CE":
            if not (9 <= len(numero) <= 12):
                raise serializers.ValidationError({"numero_documento": "El CE debe tener entre 9 y 12 caracteres."})
            if not numero.isalnum():
                raise serializers.ValidationError({"numero_documento": "El CE solo admite letras y números."})
        elif tipo == "PAS":
            if not (8 <= len(numero) <= 12):
                raise serializers.ValidationError({"numero_documento": "El Pasaporte debe tener entre 8 y 12 caracteres."})

        return data

class SolicitarOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class VerificarOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(min_length=6, max_length=6, required=True)

class ClienteReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            "email",
            "nombre",
            "apellido",
            "tipo_documento",
            "numero_documento",
            "telefono",
            "is_active",
            "email_verified",
        ]

class ClienteLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = Cliente.objects.get(email=email)
        except Cliente.DoesNotExist:
            raise serializers.ValidationError("Credenciales inválidas")

        if not user.check_password(password):
            raise serializers.ValidationError("Credenciales inválidas")

        if not user.is_active:
            raise serializers.ValidationError("La cuenta está desactivada")

        return {"user": user}
