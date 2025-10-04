from core.repositories.detalleventa_repository import DetalleVentaRepository
from core.entities.detalleventa import DetalleVenta


class ActualizarDetalleVenta:
    """Caso de uso para actualizar un detalle de venta."""

    def __init__(self, repo: DetalleVentaRepository):
        self.repo = repo

    def ejecutar(
        self,
        id: int,
        cantidad: int,
        precio_venta: float
    ) -> DetalleVenta:
        """
        Actualiza los datos de un detalle de venta existente.

        Args:
            id (int): Identificador del detalle de venta.
            cantidad (int): Nueva cantidad.
            precio_venta (float): Nuevo precio de venta.

        Returns:
            DetalleVenta: Entidad actualizada.
        """
        detalle = self.repo.get_by_id(id)
        if not detalle:
            raise ValueError(f"Detalle de venta con id {id} no encontrado")

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")

        if precio_venta < 0:
            raise ValueError("El precio de venta no puede ser negativo")

        # actualizar datos
        detalle.cantidad = cantidad
        detalle.precio_venta = precio_venta

        return self.repo.save(detalle)
