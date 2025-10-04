from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass(frozen=True)
class NotaVenta:
    """Entidad que representa una nota de venta."""

    cliente_id: int
    monto: float
    fecha: datetime = field(default_factory=datetime.now)
    activo: bool = True
    id: Optional[int] = None

    def __post_init__(self):
        """Validaciones al crear la entidad."""
        if self.monto < 0:
            raise ValueError("El monto de la nota de venta no puede ser negativo")

        if not isinstance(self.cliente_id, int) or self.cliente_id <= 0:
            raise ValueError("Debe proporcionar un cliente_id válido")

        if not isinstance(self.activo, bool):
            raise ValueError("El campo 'activo' debe ser booleano")

    @property
    def es_nueva(self) -> bool:
        """Indica si la nota de venta aún no está persistida"""
        return self.id is None

    def actualizar_monto(self, nuevo_monto: float) -> "NotaVenta":
        """Retorna una nueva instancia con el monto actualizado"""
        if nuevo_monto < 0:
            raise ValueError("El monto no puede ser negativo")
        return NotaVenta(
            id=self.id,
            cliente_id=self.cliente_id,
            monto=nuevo_monto,
            fecha=self.fecha,
            activo=self.activo
        )

    def actualizar_fecha(self, nueva_fecha: datetime) -> "NotaVenta":
        """Retorna una nueva instancia con la fecha actualizada"""
        return NotaVenta(
            id=self.id,
            cliente_id=self.cliente_id,
            monto=self.monto,
            fecha=nueva_fecha,
            activo=self.activo
        )

    def desactivar(self) -> "NotaVenta":
        """Retorna una nueva instancia marcando la nota como inactiva"""
        return NotaVenta(
            id=self.id,
            cliente_id=self.cliente_id,
            monto=self.monto,
            fecha=self.fecha,
            activo=False
        )
