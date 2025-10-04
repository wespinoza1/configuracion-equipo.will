from typing import List
from core.entities.producto import Producto
from core.repositories.producto_repository import ProductoRepository


class ListarProducto:
    """Caso de uso para listar todos los productos activos."""

    def __init__(self, repo: ProductoRepository):
        self.repo = repo

    def ejecutar(self) -> List[Producto]:
        """
        Obtiene todos los productos activos.

        Returns:
            List[Producto]: Lista de productos.
        """
        return self.repo.list_all()
