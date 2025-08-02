from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from lote.models import Lote
from lote.serializer import LoteCantidadSerializer, LoteSerializer

class LoteListView(generics.ListAPIView):
    serializer_class = LoteSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        producto_sku = self.kwargs.get('producto_sku', None)
        if producto_sku:
            return Lote.objects.filter(producto__sku=producto_sku)
        return Lote.objects.all()


class LoteCreateView(generics.CreateAPIView):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer
    permission_classes = [AllowAny]

class LoteUpdateView(generics.UpdateAPIView):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

class LoteDeleteView(generics.DestroyAPIView):
    queryset = Lote.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

class LoteCantidadUpdateView(generics.UpdateAPIView):
    queryset = Lote.objects.all()
    serializer_class = LoteCantidadSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def partial_update(self, request, *args, **kwargs):
        lote = self.get_object()
        serializer = self.get_serializer(lote, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Cantidad actualizada'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)