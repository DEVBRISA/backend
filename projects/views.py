from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from projects.models import Proyecto
from projects.serializer import ProyectoSerializer
from projects.serializer import ProyectoDeleteSerializer
from projects.serializer import ProyectoDeleteImageSerializer
from rest_framework.permissions import AllowAny as AllwoAny


class CreateProjectView(generics.CreateAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EditProjectView(generics.UpdateAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        id = kwargs.get('id')
        if not id:
            return Response({"error": "ID no proporcionado"}, status=400)

        try:
            proyecto = Proyecto.objects.get(id=id)
            data = request.data
            serializer = self.get_serializer(proyecto, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Proyecto.DoesNotExist:
            return Response({"error": "Proyecto no encontrado"}, status=status.HTTP_404_NOT_FOUND)


class DeleteProjectView(generics.DestroyAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoDeleteSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class DeleteImageView(generics.UpdateAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoDeleteImageSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        id = kwargs.get('id')
        if not id:
            return Response({"error": "ID no proporcionado"}, status=400)

        try:
            proyecto = Proyecto.objects.get(id=id)
            data = request.data
            serializer = self.get_serializer(proyecto, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Imagen(es) eliminada(s) con éxito."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Proyecto.DoesNotExist:
            return Response({"error": "Proyecto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

class ListProjectView(generics.ListAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    permission_classes = [AllwoAny]

class ProjectIdView(generics.RetrieveAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    permission_classes = [AllwoAny]
    lookup_field = 'id'

