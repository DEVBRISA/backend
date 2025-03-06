from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from empresa.models import Empresa
from empresa.serializer import EmpresaSerializer

class EmpresaListView(generics.ListAPIView):
    """ Lista todas las empresas registradas. """
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [AllowAny]

class EmpresaDetailView(generics.RetrieveAPIView):
    """ Obtiene los detalles de una empresa según su ID. """
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

class EmpresaCreateView(generics.CreateAPIView):
    """ Permite registrar una nueva empresa. """
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

class EmpresaUpdateView(generics.UpdateAPIView):
    """ Permite actualizar la información de una empresa. """
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

class EmpresaDeleteView(generics.DestroyAPIView):
    """ Permite eliminar una empresa. """
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'