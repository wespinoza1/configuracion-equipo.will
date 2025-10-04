from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class DetalleVenta:
    """
    Entidad que representa un detalle de venta
    (producto dentro de una nota de venta).
    """
    id: Optional[int]
    notaventa_id: int      # referencia a NotaVenta
    producto_id: int       # referencia a Producto
    cantidad: int
    precio_venta: float

    def __post_init__(self):
        if self.cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")
        if self.precio_venta < 0:
            raise ValueError("El precio de venta no puede ser negativo")

    @property
    def total(self) -> float:
        """Calcula el total de la línea (cantidad * precio)."""
        return self.cantidad * self.precio_venta

