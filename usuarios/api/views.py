from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from usuarios.models import Usuario
from usuarios.api.serializer import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    @action(detail=False, methods=['get'], url_path='dni/(?P<dni>\d+)')
    def get_by_dni(self, request, dni=None):
        try:
            usuario = Usuario.objects.get(dni=dni)
            serializer = self.get_serializer(usuario)
            return Response(serializer.data)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=404)

    