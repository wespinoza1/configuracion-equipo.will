from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.use_cases.registrar_detalleventa import RegistrarDetalleVenta
from core.use_cases.actualizar_detalleventa import ActualizarDetalleVenta
from core.use_cases.eliminar_detalleventa import EliminarDetalleVenta
from core.use_cases.listar_detalleventa import ListarDetalleVenta
from infrastructure.repositories.detalleventa_django_repository import DetalleVentaDjangoRepository
from api.serializers.detalleventa_serializer import DetalleVentaSerializer
from infrastructure.repositories.producto_django_repository import ProductoDjangoRepository


class DetalleVentaView(APIView):
    """CRUD para DetalleVenta"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = DetalleVentaDjangoRepository()
        self.producto_repo = ProductoDjangoRepository()

    def post(self, request):
        """Registrar un detalle de venta"""
        serializer = DetalleVentaSerializer(data=request.data)
        if serializer.is_valid():
            use_case = RegistrarDetalleVenta(self.repo, producto_repo=self.producto_repo)

            try:
                detalle = use_case.ejecutar(
                    notaventa_id=serializer.validated_data["notaventa_id"],
                    producto_id=serializer.validated_data["producto_id"],
                    cantidad=serializer.validated_data["cantidad"],
                    precio_venta=serializer.validated_data["precio_venta"],
                )
                return Response(DetalleVentaSerializer(detalle).data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                # Error de negocio: stock insuficiente u otra validación
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                return Response(
                    {"error": "Error interno del servidor"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        """
        Listar detalles de venta o ver uno solo por ID.
        """
        use_case = ListarDetalleVenta(self.repo)

        if pk:  # si viene pk, buscamos en todos los detalles
            detalles = self.repo.get_by_id(pk)
            if not detalles:
                return Response({"error": "Detalle no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            serializer = DetalleVentaSerializer(detalles)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # si no hay pk, listamos todos
        detalles = use_case.ejecutar()
        serializer = DetalleVentaSerializer(detalles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        use_case = ActualizarDetalleVenta(self.repo)

        try:
            detalle = use_case.ejecutar(
                id=pk,  # 👈 aquí va el id de la URL
                cantidad=request.data.get("cantidad"),
                precio_venta=request.data.get("precio_venta")
            )
            serializer = DetalleVentaSerializer(detalle)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        """Eliminar un detalle de venta"""
        use_case = EliminarDetalleVenta(self.repo)
        try:
            use_case.ejecutar(pk)
            return Response(status=status.HTTP_204_NO_CONTENT) # no responde nada, pero ejecuta el codigo 204
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
