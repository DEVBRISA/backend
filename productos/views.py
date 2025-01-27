from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from productos.models import Producto
from productos.serializer import ProductoDeleteImageSerializer, ProductoSerializer
from rest_framework.permissions import AllowAny

class ProductoListView(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        """Lista todos los productos"""
        productos = self.get_queryset()
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductoDetailView(generics.RetrieveAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id_producto'

    def get(self, request, id_producto=None):
        """Obtiene un producto por ID"""
        try:
            producto = self.get_queryset().get(id_producto=id_producto)
            serializer = self.get_serializer(producto)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

class ProductoCreateView(generics.CreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Crea un nuevo producto"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductoUpdateView(generics.UpdateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id_producto'

    def put(self, request, id_producto=None):
        """Actualiza un producto por ID"""
        try:
            producto = self.get_queryset().get(id_producto=id_producto)
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(producto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteProductoImageView(generics.UpdateAPIView):
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


class ProductoDeleteView(generics.DestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id_producto'

    def delete(self, request, id_producto=None):
        try:
            producto = self.get_queryset().get(id_producto=id_producto)
            producto.delete()
            return Response({"message": "Producto eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)
