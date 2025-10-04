from typing import List, Optional, Union
from core.repositories.notaventa_repository import NotaVentaRepository
from core.entities.notaventa import NotaVenta


class ListarVenta:
    """Caso de uso para listar notas de venta."""

    def __init__(self, repo: NotaVentaRepository):
        self.repo = repo

    def ejecutar(self, cliente_id: Optional[Union[int, str]] = None) -> List[NotaVenta]:
        """
        Lista notas de venta activas.

        Args:
            cliente_id (Optional[Union[int, str]]): Si se proporciona, 
            lista solo las notas de venta activas de ese cliente.

        Returns:
            List[NotaVenta]: Lista de notas de venta activas.
        """

        if cliente_id:
            return [n for n in self.repo.list_by_cliente(cliente_id) if n.activo]
        return [n for n in self.repo.list_all() if n.activo]
