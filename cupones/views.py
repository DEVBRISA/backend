from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Cupon
from .serializer import CuponSerializer


class CuponCreateView(generics.CreateAPIView):
    queryset = Cupon.objects.all()
    serializer_class = CuponSerializer
    permission_classes = [AllowAny]


class CuponUpdateView(generics.UpdateAPIView):
    queryset = Cupon.objects.all()
    serializer_class = CuponSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'


class CuponDetailView(generics.RetrieveAPIView):
    queryset = Cupon.objects.all()
    serializer_class = CuponSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'


class CuponListView(generics.ListAPIView):
    serializer_class = CuponSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Cupon.objects.all()
        activo = self.request.query_params.get('is_active')
        if activo is not None:
            queryset = queryset.filter(is_active=activo.lower() == 'true')
        return queryset


class CuponDeactivateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk):
        try:
            cupon = Cupon.objects.get(pk=pk)
        except Cupon.DoesNotExist:
            return Response({"error": "Cupón no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        cupon.is_active = False
        cupon.save()
        return Response({"mensaje": f"Cupón {cupon.codigo} desactivado con éxito."}, status=status.HTTP_200_OK)


class ValidarCuponView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        codigo = request.data.get("codigo")
        monto_compra = request.data.get("monto_compra")

        try:
            monto_compra = float(monto_compra)
        except (TypeError, ValueError):
            return Response({"error": "Monto de compra inválido."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cupon = Cupon.objects.get(codigo=codigo)
        except Cupon.DoesNotExist:
            return Response({"error": "Cupón no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        if not cupon.disponible():
            return Response({"error": "Cupón no disponible."}, status=status.HTTP_400_BAD_REQUEST)

        descuento = cupon.aplicar_descuento(monto_compra)

        cupon.usos_actuales += 1
        cupon.save()

        return Response({
            "codigo": cupon.codigo,
            "descuento": float(descuento),
            "monto_final": float(monto_compra - descuento)
        }, status=status.HTTP_200_OK)
