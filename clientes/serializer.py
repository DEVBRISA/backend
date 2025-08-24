from rest_framework import serializers
from .models import Cliente
from django.core.validators import RegexValidator

class RegistroClienteSerializer(serializers.ModelSerializer):
    otp_code = serializers.CharField(max_length=6, min_length=6, required=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    telefono = serializers.CharField(
        required=False,
        validators=[RegexValidator(r'^\+?\d{7,15}$', "Debe ser un número de teléfono válido")]
    )

    class Meta:
        model = Cliente
        fields = [
            "email",
            "otp_code",
            "nombre",
            "apellido",
            "tipo_documento",
            "numero_documento",
            "telefono",
            "password",
        ]

    def validate_tipo_documento(self, value):
        allowed = [choice[0] for choice in Cliente.TIPO_DOCUMENTO_CHOICES]  # ["DNI", "CE", "PAS"]
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
                raise serializers.ValidationError({"numero_documento": "El Carnet de Extranjería debe tener entre 9 y 12 caracteres."})
            if not numero.isalnum():
                raise serializers.ValidationError({"numero_documento": "El Carnet de Extranjería solo admite letras y números."})

        elif tipo == "PAS":
            if not (8 <= len(numero) <= 12):
                raise serializers.ValidationError({"numero_documento": "El Pasaporte debe tener entre 8 y 12 caracteres."})

        return data
