from typing import List, Optional
from core.entities.detalleventa import DetalleVenta
from core.repositories.detalleventa_repository import DetalleVentaRepository


class ListarDetalleVenta:
    """Caso de uso para listar detalles de venta."""

    def __init__(self, repo: DetalleVentaRepository):
        self.repo = repo

    def ejecutar(self, nota_venta_id: Optional[int] = None) -> List[DetalleVenta]:
        """
        Lista detalles de venta.

        Args:
            nota_venta_id (int, opcional): Si se especifica, lista solo
            los detalles de una nota de venta en particular.

        Returns:
            List[DetalleVenta]: Lista de detalles de venta encontrados.
        """
        if nota_venta_id:
            return self.repo.list_by_venta(nota_venta_id)
        return self.repo.list_all()
