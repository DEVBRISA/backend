import random
from datetime import timedelta
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import status, generics, viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cliente, OTP
from .serializer import (ClienteLoginSerializer, RegistroClienteSerializer, ClienteReadSerializer, SolicitarOTPSerializer, VerificarOTPSerializer)


# === OTP ===
class SolicitarOTPView(APIView):
    serializer_class = SolicitarOTPSerializer

    @extend_schema(
        request=SolicitarOTPSerializer,
        responses={200: OpenApiResponse(description="OTP enviado al correo")}
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        code = f"{random.randint(100000, 999999):06d}"
        OTP.objects.create(email=email, code=code)

        ctx = {"code": code, "year": timezone.now().year}
        html_body = render_to_string("emails/otp.html", ctx)
        text_body = render_to_string("emails/otp.txt", ctx)

        subject = "🔒 Código de verificación - Brisa Natural"
        msg = EmailMultiAlternatives(subject, text_body, settings.DEFAULT_FROM_EMAIL, [email])
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)

        return Response({"message": "OTP enviado al correo"}, status=status.HTTP_200_OK)


class VerificarOTPView(APIView):
    serializer_class = VerificarOTPSerializer
    @extend_schema(
        request=VerificarOTPSerializer,
        responses={
            200: OpenApiResponse(description="Correo verificado correctamente"),
            400: OpenApiResponse(description="OTP inválido o expirado")
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        otp = OTP.objects.filter(email=email, code=code, is_used=False).last()
        if not otp:
            return Response({"error": "OTP inválido"}, status=status.HTTP_400_BAD_REQUEST)

        if otp.is_expired():
            return Response({"error": "OTP expirado"}, status=status.HTTP_400_BAD_REQUEST)

        otp.is_used = True
        otp.save()
        return Response({"message": "Correo verificado correctamente"}, status=status.HTTP_200_OK)


# === Registro Cliente ===
class RegistroClienteView(generics.CreateAPIView):
    serializer_class = RegistroClienteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        cutoff = timezone.now() - timedelta(minutes=10)
        otp_ok = OTP.objects.filter(email=email, is_used=True, created_at__gte=cutoff).exists()

        if not otp_ok:
            return Response(
                {"error": "El correo no ha sido verificado o la verificación expiró"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cliente = serializer.save()
        return Response({"message": "Cliente registrado correctamente"}, status=status.HTTP_201_CREATED)


# === Gestión de clientes ===
class ClienteListView(APIView):
    def get(self, request):
        clientes = Cliente.objects.filter(is_active=True)
        serializer = ClienteReadSerializer(clientes, many=True)  # 👈 sin password
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClienteDetailByDocumentoView(APIView):
    def get(self, request, numero_documento):
        cliente = get_object_or_404(Cliente, numero_documento=numero_documento, is_active=True)
        serializer = ClienteReadSerializer(cliente)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClienteDeleteView(APIView):
    def delete(self, request, numero_documento):
        cliente = get_object_or_404(Cliente, numero_documento=numero_documento, is_active=True)
        cliente.is_active = False
        cliente.save()
        return Response({"message": "Cliente desactivado correctamente"}, status=status.HTTP_200_OK)


# === LOGIN ===
class ClienteLoginView(APIView):
    serializer_class = ClienteLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken()
        refresh["cliente_id"] = user.id
        refresh["email"] = user.email
        refresh["nombre"] = user.nombre
        refresh["apellido"] = user.apellido

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "cliente": {
                    "email": user.email,
                    "nombre": user.nombre,
                    "apellido": user.apellido,
                }
            },
            status=status.HTTP_200_OK
        )