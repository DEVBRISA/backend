from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from usuarios.models import Usuario
from usuarios.serializer import (
    LoginSerializer, RegisterSerializer, UsuarioSerializer, UsuarioChangeStateSerializer
)

class RegisterView(generics.CreateAPIView):
    """ Permite a los usuarios registrarse. No requiere autenticación. """
    queryset = Usuario.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginView(APIView):
    """ Devuelve un token de acceso y un token de actualización si las credenciales son correctas. """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        usuario = authenticate(username=username, password=password)

        if usuario:
            refresh = RefreshToken.for_user(usuario)
            return Response({
                'usuario': UsuarioSerializer(usuario).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Credenciales inválidas. Verifica tu usuario y contraseña.'}, status=status.HTTP_401_UNAUTHORIZED)

class UsuarioListView(generics.ListAPIView):
    """ Lista todos los usuarios. Solo accesible para usuarios autenticados. """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

class UsuarioDetailView(generics.RetrieveAPIView):
    """ Obtiene los detalles de un usuario según su DNI. """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'dni'

class UsuarioUpdateView(generics.UpdateAPIView):
    """ Permite actualizar parcialmente los datos de un usuario (solo PATCH). """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'dni'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_active:
            return Response({'error': 'No se puede editar un usuario inactivo.'}, status=status.HTTP_403_FORBIDDEN)

        return super().partial_update(request, *args, **kwargs)

class UsuarioChangeStateView(generics.UpdateAPIView):
    """ Activa o desactiva un usuario. """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioChangeStateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'dni'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = not instance.is_active 
        instance.save()

        estado = 'activado' if instance.is_active else 'desactivado'
        return Response({'message': f'El usuario ha sido {estado} exitosamente.', 'is_active': instance.is_active}, status=status.HTTP_200_OK)

class UsuarioDeleteView(generics.DestroyAPIView):
    """Elimina físicamente al usuario. Solo se permite si está desactivado."""
    queryset = Usuario.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'dni'

    def destroy(self, request, *args, **kwargs):
        usuario = self.get_object()

        if usuario.is_active:
            return Response({'error': 'No se puede eliminar un usuario activo. Primero desactívelo.'}, status=status.HTTP_403_FORBIDDEN)

        usuario.delete()
        return Response({'message': 'El usuario ha sido eliminado permanentemente.'}, status=status.HTTP_204_NO_CONTENT)
