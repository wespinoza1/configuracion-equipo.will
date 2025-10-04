from core.repositories.notaventa_repository import NotaVentaRepository
from core.entities.notaventa import NotaVenta
from typing import Optional
from datetime import datetime


class RegistrarVenta:
    """Caso de uso para registrar una nueva nota de venta."""

    def __init__(self, repo: NotaVentaRepository):
        self.repo = repo

    def ejecutar(self, cliente_id: int, monto: float, fecha: Optional[str] = None) -> NotaVenta:
        """
        Registra una nueva nota de venta.

        Args:
            cliente_id (int): ID del cliente al que pertenece la nota.
            monto (float): Monto total de la nota de venta.
            fecha (Optional[str]): Fecha de la nota; si no se proporciona, se usa datetime.now().

        Returns:
            NotaVenta: Instancia persistida de la nota de venta.
        """

        # Validaciones básicas
        if not isinstance(cliente_id, int) or cliente_id <= 0:
            raise ValueError("Debe proporcionar un cliente_id válido")

        if monto < 0:
            raise ValueError("El monto de la nota de venta no puede ser negativo")

        # Resolver la fecha
        if fecha:
            try:
                fecha_obj = datetime.fromisoformat(fecha)
            except ValueError:
                raise ValueError("Formato de fecha inválido, debe ser ISO 8601 (YYYY-MM-DDTHH:MM:SS)")
        else:
            fecha_obj = datetime.now()

        # Crear la nota de venta con activo=True
        nota = NotaVenta(
            cliente_id=cliente_id,
            monto=monto,
            fecha=fecha_obj,
            activo=True   # ✅ siempre activa al registrarse
        )

        # Guardar en repositorio
        return self.repo.save(nota)
