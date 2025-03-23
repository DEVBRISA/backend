from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Pack
from .serializer import (
    PackDeleteSerializer, PackSerializer, PackDeleteImageSerializer
)

class PackListView(generics.ListAPIView):
    """Obtiene la lista de packs activos."""
    serializer_class = PackSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Pack.objects.all()
        active = self.request.query_params.get('active')

        if active is not None:
            queryset = queryset.filter(active=active.lower() == 'true')

        return queryset

class PackDetailView(generics.RetrieveAPIView):
    """Obtiene el detalle de un pack activo según su SKU."""
    queryset = Pack.objects.filter(active=True)
    serializer_class = PackSerializer
    permission_classes = [AllowAny]
    lookup_field = 'sku'


class PackCreateView(generics.CreateAPIView):
    """Crea un nuevo pack."""
    queryset = Pack.objects.all()
    serializer_class = PackSerializer
    permission_classes = [AllowAny]


class PackUpdateView(generics.UpdateAPIView):
    """Actualiza un pack existente."""
    queryset = Pack.objects.all()
    serializer_class = PackSerializer
    permission_classes = [AllowAny]
    lookup_field = 'sku'


class PackDeactivateView(generics.UpdateAPIView):
    """Activa o desactiva un pack."""
    queryset = Pack.objects.all()
    serializer_class = PackDeleteSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'sku'


class PackDeleteView(generics.DestroyAPIView):
    """Elimina un pack si está inactivo."""
    queryset = Pack.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'sku'

    def destroy(self, request, *args, **kwargs):
        pack = self.get_object()
        if pack.active:
            return Response({"error": "No se puede eliminar un pack activo. Primero desactívelo."}, status=status.HTTP_403_FORBIDDEN)
        pack.delete()
        return Response({"message": "El pack ha sido eliminado permanentemente."}, status=status.HTTP_204_NO_CONTENT)


class PackDeleteImgView(generics.UpdateAPIView):
    """Elimina imágenes de un pack sin borrar el pack en sí. El true elimina la imagen. El false la mantiene"""
    queryset = Pack.objects.all()
    serializer_class = PackDeleteImageSerializer
    lookup_field = 'sku'
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        pack = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            updated_fields = []
            for field in ['img1', 'img2', 'img3', 'img4']:
                if serializer.validated_data.get(field):
                    setattr(pack, field, None)
                    updated_fields.append(field)

            pack.save(update_fields=updated_fields)
            return Response({"message": "Imagen eliminada correctamente."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
