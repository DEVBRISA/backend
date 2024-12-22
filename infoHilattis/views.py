from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from infoHilattis.models import infoHilattis
from infoHilattis.serializer import  infoHilattisSerializer
from rest_framework.permissions import AllowAny

class infoHilattisListView(generics.ListAPIView):
    queryset = infoHilattis.objects.all()
    serializer_class = infoHilattisSerializer
    permission_classes = [AllowAny]

class infoHilattisCreateView(generics.CreateAPIView):
    queryset = infoHilattis.objects.all()
    serializer_class = infoHilattisSerializer
    permission_classes = [IsAuthenticated]  

class infoHilattisUpdateView(generics.UpdateAPIView):
    queryset = infoHilattis.objects.all()
    serializer_class = infoHilattisSerializer
    permission_classes = [IsAuthenticated]  
    lookup_field = 'id' 

