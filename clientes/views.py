from datetime import date
from django.conf import settings
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cliente
from .serializer import (
    ClienteLoginSerializer,
    ClienteReadSerializer,
    RegistroClienteSerializer
)


# === Registro Cliente ===
class RegistroClienteView(generics.CreateAPIView):
    serializer_class = RegistroClienteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # ✅ Si pasa validaciones (incluye edad), lo guardamos
        cliente = serializer.save()
        return Response(
            {"message": "Cliente registrado correctamente"},
            status=status.HTTP_201_CREATED,
        )


# === Gestión de clientes ===
class ClienteListView(APIView):
    def get(self, request):
        clientes = Cliente.objects.filter(is_active=True)
        serializer = ClienteReadSerializer(clientes, many=True)  # 👈 sin password
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClienteDetailByDocumentoView(APIView):
    def get(self, request, numero_documento):
        cliente = get_object_or_404(
            Cliente, numero_documento=numero_documento, is_active=True
        )
        serializer = ClienteReadSerializer(cliente)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClienteDeleteView(APIView):
    def delete(self, request, numero_documento):
        cliente = get_object_or_404(
            Cliente, numero_documento=numero_documento, is_active=True
        )
        cliente.is_active = False
        cliente.save()
        return Response(
            {"message": "Cliente desactivado correctamente"},
            status=status.HTTP_200_OK,
        )


# === LOGIN ===
class ClienteLoginView(APIView):
    serializer_class = ClienteLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
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
                },
            },
            status=status.HTTP_200_OK,
        )
