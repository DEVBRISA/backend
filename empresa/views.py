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

class EmpresaCreateView(generics.CreateAPIView):
    """ Permite crear una nueva empresa. """
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated]

class EmpresaDetailView(generics.RetrieveAPIView):
    """ Obtiene los detalles de una empresa según su ID. """
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

class EmpresaUpdateView(generics.UpdateAPIView):
    """ Permite actualizar la información de una empresa. """
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'