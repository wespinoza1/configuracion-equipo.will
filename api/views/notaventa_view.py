from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers.notaventa_serializer import NotaVentaSerializer
from infrastructure.repositories.notaventa_django_repository import NotaVentaDjangoRepository
from core.use_cases.registrar_venta import RegistrarVenta
from core.use_cases.actualizar_venta import ActualizarVenta
from core.use_cases.eliminar_venta import EliminarVenta
from core.use_cases.listar_venta import ListarVenta


class NotaVentaView(APIView):
    """
    Endpoints para gestionar Notas de Venta.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = NotaVentaDjangoRepository()

    def get(self, request, pk=None):
        """
        Lista todas las notas de venta o filtra por cliente.
        """
        use_case = ListarVenta(self.repo)

        if pk:  # si viene un id en la URL
            notas = self.repo.get_by_id(pk)  # necesitas implementar este método en el repo
            if not notas:
                return Response({"error": "Nota de venta no encontrada"}, status=status.HTTP_404_NOT_FOUND)
            serializer = NotaVentaSerializer(notas)
        else:
            notas = use_case.ejecutar()
            serializer = NotaVentaSerializer(notas, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Registra una nueva nota de venta.
        """
        serializer = NotaVentaSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            use_case = RegistrarVenta(self.repo)
            nota = use_case.ejecutar(
                cliente_id=data["cliente_id"],  # ✅ solo el id
                monto=data["monto"],
                fecha=request.data.get("fecha")  # opcional
            )

            return Response(NotaVentaSerializer(nota).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Actualiza una nota de venta existente.
        """
        serializer = NotaVentaSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            use_case = ActualizarVenta(self.repo)
            nota = use_case.ejecutar(
                id=pk,  # aquí ya le pasas pk como id
                cliente_id=data.get("cliente_id"),
                monto=data.get("monto"),
                fecha=request.data.get("fecha")  # opcional
            )

            if not nota:
                return Response({"error": "Nota de venta no encontrada"}, status=status.HTTP_404_NOT_FOUND)

            return Response(NotaVentaSerializer(nota).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Elimina (soft delete) una nota de venta.
        """
        use_case = EliminarVenta(self.repo)
        try:
            use_case.ejecutar(pk)
            return Response({"mensaje": f"Nota de venta {pk} eliminada correctamente"}, 
                        status=status.HTTP_200_OK) 
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
