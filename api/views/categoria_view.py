from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers.categoria_serializer import CategoriaSerializer
from core.entities.categoria import Categoria
from core.use_cases.registrar_categoria import RegistrarCategoria
from infrastructure.repositories.categoria_django_repository import CategoriaDjangoRepository


class CategoriaView(APIView):
    """Vista para manejar Categorías (CRUD)."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = CategoriaDjangoRepository()

    def get(self, request, pk=None):
        """Listar todas o una categoría por id."""
        if pk:
            categoria = self.repo.get_by_id(pk)
            if not categoria:
                return Response({"detail": "Categoría no encontrada"}, status=status.HTTP_404_NOT_FOUND)
            serializer = CategoriaSerializer(categoria.__dict__)
            return Response(serializer.data)
        else:
            categorias = self.repo.list_all()
            serializer = CategoriaSerializer([c.__dict__ for c in categorias], many=True)
            return Response(serializer.data)

    def post(self, request):
        """Crear una categoría."""
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            use_case = RegistrarCategoria(self.repo)
            try:
                categoria = use_case.ejecutar(
                    nombre=serializer.validated_data["nombre"],
                    activa=serializer.validated_data.get("activa", True),
                )
                return Response(CategoriaSerializer(categoria.__dict__).data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Actualizar categoría existente."""
        categoria = self.repo.get_by_id(pk)
        if not categoria:
            return Response({"detail": "Categoría no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            actualizado = categoria.activar() if serializer.validated_data.get("activa", True) else categoria.desactivar()
            actualizado = Categoria(
                id=categoria.id,
                nombre=serializer.validated_data["nombre"],
                fecha_creacion=categoria.fecha_creacion,
                activa=actualizado.activa,
            )
            actualizado = self.repo.save(actualizado)
            return Response(CategoriaSerializer(actualizado.__dict__).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        """Eliminar (soft delete) una categoría."""
        try:
            categoria = self.repo.get_by_id(pk)
            if not categoria:
                return Response(
                    {"detail": "Categoría no encontrada"}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # Usamos soft delete
            self.repo.delete(pk)

            # Mensaje de confirmación
            nombre = categoria.nombre or "sin nombre"
            return Response(
                {"detail": f"La categoría '{nombre}' ha sido desactivada correctamente."},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            # Capturamos cualquier error inesperado
            return Response(
                {"detail": f"Error al desactivar la categoría: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )





