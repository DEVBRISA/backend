from datetime import timedelta
import random
from django.utils import timezone
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password

from clientes.serializer import RegistroClienteSerializer
from .models import OTP, Cliente

class SolicitarOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email requerido"}, status=status.HTTP_400_BAD_REQUEST)

        code = str(random.randint(100000, 999999))
        OTP.objects.create(email=email, code=code)

        ctx = {"code": code, "year": timezone.now().year}
        html_body = render_to_string("emails/otp.html", ctx)
        text_body = render_to_string("emails/otp.txt", ctx)

        subject = "🔒 Código de verificación - Brisa Natural"
        from_email = settings.DEFAULT_FROM_EMAIL
        to = [email]

        msg = EmailMultiAlternatives(subject, text_body, from_email, to)
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)

        return Response({"message": "OTP enviado al correo"}, status=status.HTTP_200_OK)


class VerificarOTPView(APIView):
    """Verifica el OTP enviado al correo"""

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        otp = OTP.objects.filter(email=email, code=code, is_used=False).last()
        if not otp:
            return Response({"error": "OTP inválido"}, status=status.HTTP_400_BAD_REQUEST)

        if otp.is_expired():
            return Response({"error": "OTP expirado"}, status=status.HTTP_400_BAD_REQUEST)

        otp.is_used = True
        otp.save()
        return Response({"message": "Correo verificado correctamente"}, status=status.HTTP_200_OK)


class RegistroClienteView(APIView):
    serializer_class = RegistroClienteSerializer

    def get(self, request, *args, **kwargs):
        """Para que el Browsable API muestre el form en GET"""
        serializer = self.serializer_class()
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp_code = serializer.validated_data["otp_code"]

        try:
            otp = OTP.objects.filter(email=email, code=otp_code).latest("created_at")
        except OTP.DoesNotExist:
            return Response({"error": "Código inválido"}, status=status.HTTP_400_BAD_REQUEST)

        if timezone.now() > otp.created_at + timedelta(minutes=10):
            return Response({"error": "Código expirado"}, status=status.HTTP_400_BAD_REQUEST)

        cliente = Cliente.objects.create(
            email=email,
            nombre=serializer.validated_data["nombre"],
            apellido=serializer.validated_data["apellido"],
            tipo_documento=serializer.validated_data["tipo_documento"],
            numero_documento=serializer.validated_data["numero_documento"],
            telefono=serializer.validated_data.get("telefono"),
        )
        cliente.set_password(serializer.validated_data["password"])
        cliente.save()

        return Response({"message": "Cliente registrado correctamente"}, status=status.HTTP_201_CREATED)