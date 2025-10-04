from core.entities.producto import Producto
from core.repositories.producto_repository import ProductoRepository


class EliminarProducto:
    """Caso de uso para eliminar (soft delete) un producto."""

    def __init__(self, repo: ProductoRepository):
        self.repo = repo

    def ejecutar(self, producto: Producto) -> None:
        """
        Elimina (desactiva) un producto existente.

        Args:
            producto (Producto): Entidad del producto a eliminar.

        Returns:
            None
        """

        if not producto.id:
            raise ValueError("El producto debe tener un ID válido para ser eliminado")

        # Delegamos al repositorio, que aplica soft delete
        self.repo.delete(producto.id)
