from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from usuarios.models import Usuario
from usuarios.api.serializer import LoginSerializer, RegisterSerializer, UsuarioSerializer, UsuarioChangeStateSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

class RegisterView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """devuelve un token de acceso y un token de actualización"""
        username = request.data.get("username")
        password = request.data.get("password")
        usuario = authenticate(username=username, password=password)

        if usuario is not None:
            refresh = RefreshToken.for_user(usuario)
            user_serializer = UsuarioSerializer(usuario)
            return Response({
                'usuario': user_serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Credenciales inválidas'}, status=401)
        

class UsuarioListView(generics.ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer 
    permission_classes = [IsAuthenticated] 


class UsuarioDetailView(generics.RetrieveAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]  
    lookup_field = 'dni'  


class UsuarioUpdateView(generics.UpdateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'dni'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_active:
            return Response({'error': 'No se puede editar un usuario inactivo.'}, status=403)
        return super().update(request, *args, **kwargs)

class UsuarioChangeStateView(generics.UpdateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioChangeStateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'dni'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        # Validación y guardado
        serializer.is_valid(raise_exception=True)
        serializer.save()

        estado = 'activado' if instance.is_active else 'desactivado'
        return Response({'message': f'El usuario ha sido {estado} exitosamente.'}, status=200)

class UsuarioDeleteView(generics.DestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'dni'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_active:
            return Response({'error': 'No se puede eliminar un usuario activo.'}, status=403)
        return super().destroy(request, *args, **kwargs)
