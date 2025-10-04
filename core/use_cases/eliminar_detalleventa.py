from core.repositories.detalleventa_repository import DetalleVentaRepository


class EliminarDetalleVenta:
    """Caso de uso para eliminar un detalle de venta."""

    def __init__(self, repo: DetalleVentaRepository):
        self.repo = repo

    def ejecutar(self, id: int) -> None:
        """
        Elimina un detalle de venta existente.

        Args:
            id (int): Identificador del detalle de venta a eliminar.

        Raises:
            ValueError: Si el detalle de venta no existe.
        """
        detalle = self.repo.get_by_id(id)
        if not detalle:
            raise ValueError(f"Detalle de venta con id {id} no encontrado")

        self.repo.delete(id)
