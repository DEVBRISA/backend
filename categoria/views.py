from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from categoria.models import Categoria
from categoria.serializer import CategoriaSerializer
from rest_framework.permissions import AllowAny


class CategoriaListView(generics.ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        """Lista todas las categorías"""
        categorias = self.get_queryset()
        serializer = self.get_serializer(categorias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoriaIdView(generics.RetrieveAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

    def get(self, request, id=None):
        """Obtiene una categoría por ID"""
        try:
            categoria = self.get_queryset().get(id=id)
            serializer = self.get_serializer(categoria)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Categoria.DoesNotExist:
            return Response({"error": "Categoría no encontrada"}, status=status.HTTP_404_NOT_FOUND)

class CategoriaCreateView(generics.CreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Crea una nueva categoría"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoriaEditView(generics.UpdateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        id = kwargs.get('id')
        if not id:
            return Response({"error": "ID no proporcionado"}, status=400)
        
        try:
            categoria = Categoria.objects.get(id=id)
            data = request.data
            
            if 'imagen' not in data:
                data['imagen'] = categoria.imagen  
            serializer = self.get_serializer(categoria, data=data, partial=True)  
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Categoria.DoesNotExist:
            return Response({"error": "Categoría no encontrada"}, status=status.HTTP_404_NOT_FOUND)

class CategoriaDeleteView(generics.DestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def delete(self, request, id=None):
        """Elimina una categoría por ID"""
        try:
            categoria = self.get_queryset().get(id=id)
            categoria.delete()
            return Response({"message": "Categoría eliminada exitosamente"}, status=status.HTTP_204_NO_CONTENT)
        except Categoria.DoesNotExist:
            return Response({"error": "Categoría no encontrada"}, status=status.HTTP_404_NOT_FOUND)
