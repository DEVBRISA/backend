import cloudinary.uploader
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Producto
from .serializer import (
    ProductoPackSerializer, ProductoSerializer, ProductoDeleteSerializer, ProductoDeleteImageSerializer
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
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    lookup_field = 'sku'

    def get_queryset(self):
        return Producto.objects.all()


class ProductoCreateView(generics.CreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        img_urls = {}

        for img_field in ['img1', 'img2', 'img3', 'img4']:
            file = self.request.FILES.get(img_field)
            if file:
                result = cloudinary.uploader.upload(file)
                img_urls[img_field] = result.get('secure_url')

        serializer.save(**img_urls)


class ProductoUpdateView(generics.UpdateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]
    lookup_field = 'sku'

    def perform_update(self, serializer):
        img_urls = {}

        for img_field in ['img1', 'img2', 'img3', 'img4']:
            file = self.request.FILES.get(img_field)
            if file:
                result = cloudinary.uploader.upload(file)
                img_urls[img_field] = result.get('secure_url')

        serializer.save(**img_urls)
        

class ProductoDeactivateView(generics.UpdateAPIView):
    """Activa o desactiva un producto."""
    queryset = Producto.objects.all()
    serializer_class = ProductoDeleteSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'sku'


class ProductoDeleteView(generics.DestroyAPIView):
    """Elimina un producto si está inactivo."""
    queryset = Producto.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'sku'

    def destroy(self, request, *args, **kwargs):
        producto = self.get_object()
        if producto.active:
            return Response({"error": "No se puede eliminar un producto activo. Primero desactívelo."}, status=status.HTTP_403_FORBIDDEN)
        producto.delete()
        return Response({"message": "El producto ha sido eliminado permanentemente."}, status=status.HTTP_204_NO_CONTENT)


class ProductoDeleteImgView(generics.UpdateAPIView):
    """Elimina imágenes de un producto sin borrar el producto en sí.El true elimina la imagen. El false la mantiene"""
    queryset = Producto.objects.all()
    serializer_class = ProductoDeleteImageSerializer
    lookup_field = 'sku'
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        producto = self.get_object()
        serializer = self.get_serializer(producto, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Imagen eliminada correctamente."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProductoTogglePackView(generics.UpdateAPIView):
    """Activa un producto para que sea parte del apartado 'PACK RUTINA'"""
    queryset = Producto.objects.all()
    serializer_class = ProductoPackSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'sku'

    def patch(self, request, *args, **kwargs):
        producto = self.get_object()
        pack_estado = request.data.get('pack')
        
        if pack_estado is not None:
            producto.pack = pack_estado
            producto.save()
            return Response({"message": "Estado de pack actualizado correctamente."}, status=200)
        
        return Response({"error": "Debe proporcionar el campo 'pack'."}, status=400)

