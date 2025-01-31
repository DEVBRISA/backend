from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from productos.models import Producto
from variants.models import Variante
from variants.serializer import VarianteSerializer, VarianteDeleteImageSerializer

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
        

class VarianteListByProductView(generics.ListAPIView):
    serializer_class = VarianteSerializer
    permission_classes = [AllowAny]

    def get(self, request, id_producto=None):
        """Obtiene todas las variantes de un producto específico"""
        if id_producto is not None:
            # Aquí filtras las variantes directamente por el campo 'producto'
            variantes = Variante.objects.filter(producto=id_producto)
            serializer = self.get_serializer(variantes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Si no se pasa un id_producto, se devuelven todas las variantes
            variantes = self.get_queryset()
            serializer = self.get_serializer(variantes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class VarianteCreateView(generics.CreateAPIView):
    queryset = Variante.objects.all()
    serializer_class = VarianteSerializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]
    lookup_field = 'id_variante'

    def patch(self, request, id_variante=None):
        """Actualiza una variante por ID parcialmente"""
        try:
            variante = self.get_queryset().get(id_variante=id_variante)
        except Variante.DoesNotExist:
            return Response({"error": "Variante no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(variante, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class DeleteVarianteImageView(generics.UpdateAPIView):
    queryset = Variante.objects.all()
    serializer_class = VarianteDeleteImageSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id_variante'

    def put(self, request, *args, **kwargs):
        id_variante = kwargs.get('id_variante')
        if not id_variante:
            return Response({"error": "ID de variante no proporcionado"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            variante = Variante.objects.get(id_variante=id_variante)
            data = request.data
            serializer = self.get_serializer(variante, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Imagen(es) eliminada(s) con éxito."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Variante.DoesNotExist:
            return Response({"error": "Variante no encontrada"}, status=status.HTTP_404_NOT_FOUND)


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
