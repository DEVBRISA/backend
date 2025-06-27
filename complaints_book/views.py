from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Reclamo
from .serializer import ReclamoSerializer

class ReclamoCreateView(generics.CreateAPIView):
    queryset = Reclamo.objects.all()
    serializer_class = ReclamoSerializer
    permission_classes = [AllowAny]

class ReclamoListView(generics.ListAPIView):
    queryset = Reclamo.objects.all().order_by('-fecha_envio')
    serializer_class = ReclamoSerializer
    permission_classes = [IsAuthenticated]
