from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Producto
from .serializer import (
    ProductoSerializer, ProductoDeleteSerializer, ProductoDeleteImageSerializer
)

class ProductoListView(generics.ListAPIView):
    """Obtiene la lista de productos activos y visibles."""
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Producto.objects.all()
        active = self.request.query_params.get('active')

        if active is not None:
            queryset = queryset.filter(active=active.lower() == 'true')

        return queryset

class ProductoDetailView(generics.RetrieveAPIView):
    """Obtiene el detalle de un producto activo según su SKU."""
    queryset = Producto.objects.filter(active=True)
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]
    lookup_field = 'sku'


class ProductoCreateView(generics.CreateAPIView):
    """Crea un nuevo producto."""
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]


class ProductoUpdateView(generics.UpdateAPIView):
    """Actualiza un producto existente."""
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]
    lookup_field = 'sku'

class ProductoDeactivateView(generics.UpdateAPIView):
    """Activa o desactiva un producto."""
    queryset = Producto.objects.all()
    serializer_class = ProductoDeleteSerializer
    permission_classes = [AllowAny]
    lookup_field = 'sku'


class ProductoDeleteView(generics.DestroyAPIView):
    """Elimina un producto si está inactivo."""
    queryset = Producto.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'sku'

    def destroy(self, request, *args, **kwargs):
        producto = self.get_object()
        if producto.active:
            return Response({"error": "No se puede eliminar un producto activo. Primero desactívelo."}, status=status.HTTP_403_FORBIDDEN)
        producto.delete()
        return Response({"message": "El producto ha sido eliminado permanentemente."}, status=status.HTTP_204_NO_CONTENT)


class ProductoDeleteImgView(generics.UpdateAPIView):
    """Elimina imágenes de un producto sin borrar el producto en sí."""
    queryset = Producto.objects.all()
    serializer_class = ProductoDeleteImageSerializer
    lookup_field = 'sku'
    permission_classes = [AllowAny]

    def patch(self, request, *args, **kwargs):
        producto = self.get_object()
        serializer = self.get_serializer(producto, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Imagen eliminada correctamente."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
