from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Promocion
from offer.serializer import PromocionSerializer


class PromocionListView(generics.ListAPIView):
    """
    Lista todas las promociones registradas.
    Puedes filtrar por:
    - `activa`: `true` o `false` para mostrar solo promociones activas o inactivas.
    - `producto_id`: ID de un producto específico para filtrar promociones que aplican a ese producto.
    - `categoria_id`: ID de una categoría específica para filtrar promociones aplicables a esa categoría."""

    serializer_class = PromocionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Promocion.objects.all()

        activa = self.request.query_params.get('activa')
        if activa is not None:
            queryset = queryset.filter(activa=activa.lower() == 'true')

        producto_id = self.request.query_params.get('producto_id')
        if producto_id is not None:
            queryset = queryset.filter(producto_id=producto_id)

        categoria_id = self.request.query_params.get('categoria_id')
        if categoria_id is not None:
            queryset = queryset.filter(categoria_id=categoria_id)

        return queryset

    
class PromocionDetailView(generics.RetrieveAPIView):
    """
    Obtiene el detalle de una promoción específica por su ID.
    """
    queryset = Promocion.objects.all()
    serializer_class = PromocionSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'


class PromocionCreateView(generics.CreateAPIView):
    """
    Crea una nueva promoción en el sistema.

    - `tipo`: `combo` o `descuento`.
    - `activa`: `true` o `false`.
    - **Uno de los dos:** `producto` o `categoria`.
    """
    queryset = Promocion.objects.all()
    serializer_class = PromocionSerializer
    permission_classes = [AllowAny]


class PromocionUpdateView(generics.UpdateAPIView):
    """
    Actualiza los datos de una promoción existente.
    """
    queryset = Promocion.objects.all()
    serializer_class = PromocionSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'



class PromocionDeleteView(generics.DestroyAPIView):
    """
    Elimina una promoción del sistema por su ID.
    """
    queryset = Promocion.objects.all()
    serializer_class = PromocionSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'





