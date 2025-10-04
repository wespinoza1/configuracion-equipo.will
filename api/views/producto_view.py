from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.use_cases.registrar_producto import RegistrarProducto
from core.use_cases.actualizar_producto import ActualizarProducto
from core.use_cases.eliminar_producto import EliminarProducto
from core.use_cases.listar_producto import ListarProducto

from infrastructure.repositories.producto_django_repository import ProductoDjangoRepository
from infrastructure.repositories.categoria_django_repository import CategoriaDjangoRepository
from api.serializers.producto_serializer import ProductoSerializer


class ProductoView(APIView):
    """CRUD de productos con casos de uso."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = ProductoDjangoRepository()
        self.categoria_repo = CategoriaDjangoRepository()

    def get(self, request, pk=None):
        use_case = ListarProducto(self.repo)

        if pk:
            producto = self.repo.get_by_id(pk)
            if not producto:
                return Response({"detail": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            serializer = ProductoSerializer(producto)
            return Response(serializer.data)
        else:
            productos = use_case.ejecutar()
            serializer = ProductoSerializer(productos, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            # usar el campo plano categoria_id que definimos
            categoria_id = serializer.validated_data["categoria_id"]
            categoria = self.categoria_repo.get_by_id(categoria_id)
            if not categoria or not categoria.activa:
                return Response({"detail": "Categoría inválida o inactiva"}, status=status.HTTP_400_BAD_REQUEST)

            use_case = RegistrarProducto(self.repo)
            try:
                producto = use_case.ejecutar(
                    descripcion=serializer.validated_data["descripcion"],
                    precio=serializer.validated_data["precio"],
                    stock=serializer.validated_data["stock"],
                    categoria=categoria
                )
                return Response(ProductoSerializer(producto).data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        producto = self.repo.get_by_id(pk)
        if not producto:
            return Response({"detail": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            categoria_id = serializer.validated_data["categoria_id"]

            # validar categoría en la vista (puedes delegar esto al use case si prefieres)
            categoria = self.categoria_repo.get_by_id(categoria_id)
            if not categoria or not categoria.activa:
                return Response({"detail": "Categoría inválida o inactiva"}, status=status.HTTP_400_BAD_REQUEST)

            use_case = ActualizarProducto(self.repo, self.categoria_repo)
            try:
                actualizado = use_case.ejecutar(
                    producto_id=producto.id,
                    descripcion=serializer.validated_data["descripcion"],
                    precio=serializer.validated_data["precio"],
                    stock=serializer.validated_data["stock"],
                    categoria_id=categoria_id,
                    activo=serializer.validated_data.get("activo", producto.activo)
                )
                return Response(ProductoSerializer(actualizado).data, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        producto = self.repo.get_by_id(pk)
        if not producto:
            return Response({"detail": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        use_case = EliminarProducto(self.repo)
        use_case.ejecutar(producto)

        return Response(
            {"detail": f"El producto '{producto.descripcion}' ha sido desactivado correctamente."},
            status=status.HTTP_200_OK
        )
