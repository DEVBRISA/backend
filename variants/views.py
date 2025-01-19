from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from variants.models import Variante
from variants.serializer import VarianteSerializer

class VarianteListView(generics.ListAPIView):
    queryset = Variante.objects.all()
    serializer_class = VarianteSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        """Lista todas las variantes"""
        variantes = self.get_queryset()
        serializer = self.get_serializer(variantes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VarianteDetailView(generics.RetrieveAPIView):
    queryset = Variante.objects.all()
    serializer_class = VarianteSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id_variante'

    def get(self, request, id_variante=None):
        """Obtiene una variante por ID"""
        try:
            variante = self.get_queryset().get(id_variante=id_variante)
            serializer = self.get_serializer(variante)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Variante.DoesNotExist:
            return Response({"error": "Variante no encontrada"}, status=status.HTTP_404_NOT_FOUND)


class VarianteCreateView(generics.CreateAPIView):
    queryset = Variante.objects.all()
    serializer_class = VarianteSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """Crea una nueva variante"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VarianteUpdateView(generics.UpdateAPIView):
    queryset = Variante.objects.all()
    serializer_class = VarianteSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id_variante'

    def put(self, request, id_variante=None):
        """Actualiza una variante por ID"""
        try:
            variante = self.get_queryset().get(id_variante=id_variante)
        except Variante.DoesNotExist:
            return Response({"error": "Variante no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(variante, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VarianteDeleteView(generics.DestroyAPIView):
    queryset = Variante.objects.all()
    serializer_class = VarianteSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id_variante'

    def delete(self, request, id_variante=None):
        """Elimina una variante por ID"""
        try:
            variante = self.get_queryset().get(id_variante=id_variante)
            variante.delete()
            return Response({"message": "Variante eliminada correctamente"}, status=status.HTTP_204_NO_CONTENT)
        except Variante.DoesNotExist:
            return Response({"error": "Variante no encontrada"}, status=status.HTTP_404_NOT_FOUND)
