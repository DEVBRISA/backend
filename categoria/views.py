from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from categoria.models import Categoria
from categoria.serializer import (
    CategoriaDeleteSerializer, CategoriaSerializer, ToggleCategoriaVisibilitySerializer
)

class CategoriaListView(generics.ListAPIView):
    """Obtiene la lista de categorías registradas."""
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]

class CategoriaDetailView(generics.RetrieveAPIView):
    """Obtiene los detalles de una categoría específica mediante su ID."""
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

class CategoriaCreateView(generics.CreateAPIView):
    """Crea una nueva categoría (requiere autenticación)."""
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        nombre = request.data.get('nombre', '').strip()
        if Categoria.objects.filter(nombre__iexact=nombre).exists():
            return Response({"error": "Ya existe una categoría con este nombre."}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

class CategoriaUpdateView(generics.UpdateAPIView):
    """Modifica parcialmente los datos de una categoría (requiere autenticación)."""
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        categoria = self.get_object()
        serializer = self.get_serializer(categoria, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ToggleCategoriaVisibilityView(generics.UpdateAPIView):
    """Activa o desactiva la visibilidad de una categoría (requiere autenticación)."""
    queryset = Categoria.objects.all()
    serializer_class = ToggleCategoriaVisibilitySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        categoria = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            categoria.visible = serializer.validated_data['visible']
            categoria.save()
            estado = "visible" if categoria.visible else "oculta"
            return Response({"message": f"Categoría ahora está {estado}."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoriaDeactivateView(generics.UpdateAPIView):
    """Desactiva una categoría en lugar de eliminarla físicamente."""
    queryset = Categoria.objects.all()
    serializer_class = CategoriaDeleteSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        categoria = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            categoria.active = serializer.validated_data['active']
            categoria.save()
            estado = "activa" if categoria.active else "inactiva"
            return Response({"message": f"Categoría ahora está {estado}."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoriaDeleteView(generics.DestroyAPIView):
    """Elimina una categoría definitivamente solo si está inactiva."""
    queryset = Categoria.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        categoria = self.get_object()

        if categoria.active:
            return Response(
                {"error": "No se puede eliminar una categoría activa. Primero desactívela."},
                status=status.HTTP_403_FORBIDDEN
            )

        categoria.delete()
        return Response({"message": "La categoría ha sido eliminada permanentemente."}, status=status.HTTP_204_NO_CONTENT)

