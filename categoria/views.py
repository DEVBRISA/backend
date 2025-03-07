from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from categoria.models import Categoria
from categoria.serializer import CategoriaSerializer

class CategoriaListView(generics.ListCreateAPIView):
    """ Lista todas las categorías o permite crear una nueva. """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]

class CategoriaDetailView(generics.RetrieveAPIView):
    """ Obtiene los detalles de una categoría específica. """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

class CategoriaCreateView(generics.CreateAPIView):
    """ Crea una nueva categoría. """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]

class CategoriaUpdateView(generics.UpdateAPIView):
    """ Actualiza una categoría específica. """
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
    """ Elimina una categoría específica. """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'