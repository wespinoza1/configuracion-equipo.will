from typing import Union
from core.repositories.notaventa_repository import NotaVentaRepository
from core.entities.notaventa import NotaVenta


class EliminarVenta:
    """Caso de uso para eliminar (soft o hard) una nota de venta."""

    def __init__(self, repo: NotaVentaRepository):
        self.repo = repo

    def ejecutar(self, id: Union[int, str], soft: bool = True) -> NotaVenta:
        """
        Elimina una nota de venta existente.

        Args:
            id (Union[int, str]): Identificador único de la nota de venta.
            soft (bool): Si es True, realiza un soft delete; si es False, hard delete.

        Returns:
            NotaVenta: La nota de venta eliminada (con activo=False si es soft).

        Raises:
            ValueError: Si la nota de venta no existe.
        """

        # Verificar que exista la nota
        nota_existente = self.repo.get_by_id(id)
        if not nota_existente:
            raise ValueError(f"No se encontró la nota de venta con id={id}")

        if soft:
            # Marcar como inactiva
            nota_inactiva = NotaVenta(
                id=nota_existente.id,
                cliente_id=nota_existente.cliente_id,
                monto=nota_existente.monto,
                fecha=nota_existente.fecha,
                activo=False
            )
            return self.repo.save(nota_inactiva)

        # Hard delete
        self.repo.delete(id, soft=False)
        return nota_existente
