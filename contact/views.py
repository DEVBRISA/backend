from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Contacto
from contact.serializer import ContactoSerializer

class ContactoListView(generics.ListAPIView):
    """Obtiene la lista de mensajes de contacto."""
    queryset = Contacto.objects.all().order_by('-fecha_envio')
    serializer_class = ContactoSerializer
    permission_classes = [IsAuthenticated]

class ContactoCreateView(generics.CreateAPIView):
    """Crea un nuevo mensaje de contacto."""
    queryset = Contacto.objects.all()
    serializer_class = ContactoSerializer
    permission_classes = [AllowAny]
