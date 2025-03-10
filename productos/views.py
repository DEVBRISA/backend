from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Producto
from .serializer import (
    ProductoDeleteImageSerializer, ProductoSerializer, ProductoDeleteSerializer, ToggleProductoVisibilitySerializer
)

class ProductoListView(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]

class ProductoDetailView(generics.RetrieveAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]
    lookup_field = 'sku'

class ProductoCreateView(generics.CreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

class ProductoUpdateView(generics.UpdateAPIView):
    queryset = Producto.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'sku'

    def patch(self, request, *args, **kwargs):
        producto = self.get_object()
        serializer = self.get_serializer(producto, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ToggleProductoVisibilityView(generics.UpdateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ToggleProductoVisibilitySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'sku'

    def patch(self, request, *args, **kwargs):
        producto = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            producto.visible = serializer.validated_data['visible']
            producto.save()
            estado = "visible" if producto.visible else "oculto"
            return Response({"message": f"El producto ahora está {estado}."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductoDeactivateView(generics.UpdateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoDeleteSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'sku'

    def patch(self, request, *args, **kwargs):
        producto = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            producto.active = serializer.validated_data['active']
            producto.save()
            estado = "activo" if producto.active else "inactivo"
            return Response({"message": f"El producto ahora está {estado}."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductoDeleteView(generics.DestroyAPIView):
    queryset = Producto.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'sku'

    def destroy(self, request, *args, **kwargs):
        producto = self.get_object()
        
        if producto.active:
            return Response(
                {"error": "No se puede eliminar un producto activo. Primero desactívelo."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        producto.delete()
        return Response({"message": "El producto ha sido eliminado permanentemente."}, status=status.HTTP_204_NO_CONTENT)

class ProductoDeleteImgView(generics.UpdateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoDeleteImageSerializer
    lookup_field = 'id_producto'
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        id = kwargs.get('id')
        if not id:
            return Response({"error": "ID no proporcionado"}, status=400)

        try:
            producto = Producto.objects.get(id=id)
            data = request.data
            serializer = self.get_serializer(producto, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Imagen eliminada con éxito."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)


