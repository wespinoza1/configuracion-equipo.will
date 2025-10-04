from core.repositories.detalleventa_repository import DetalleVentaRepository
from core.repositories.producto_repository import ProductoRepository
from core.entities.detalleventa import DetalleVenta
from typing import Optional


class RegistrarDetalleVenta:
    """Caso de uso para registrar un detalle de venta."""

    def __init__(self, repo: DetalleVentaRepository, producto_repo: ProductoRepository):
        self.repo = repo
        self.producto_repo = producto_repo

    def ejecutar(
        self,
        notaventa_id: int,
        producto_id: int,
        cantidad: int,
        precio_venta: float,
        id: Optional[int] = None
    ) -> DetalleVenta:
        """
        Crea un nuevo detalle de venta asociado a una nota de venta.

        Args:
            notaventa_id (int): Identificador de la nota de venta.
            producto_id (int): Identificador del producto.
            cantidad (int): Cantidad de productos.
            precio_venta (float): Precio unitario de venta.
            id (Optional[int]): Identificador (solo para actualización).

        Returns:
            DetalleVenta: Entidad creada.
        """

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")

        if precio_venta < 0:
            raise ValueError("El precio de venta no puede ser negativo")
        

        # 1. Buscar producto
        producto = self.producto_repo.get_by_id(producto_id)
        if producto is None:
            raise ValueError("El producto no existe")

        # 2. Validar y disminuir stock
        producto_actualizado = producto.disminuir_stock(cantidad)

        # 3. Guardar el producto actualizado
        self.producto_repo.save(producto_actualizado)

        # 4. Crear detalle de venta
        detalle = DetalleVenta(
            id=id,
            notaventa_id=notaventa_id,
            producto_id=producto_id,
            cantidad=cantidad,
            precio_venta=precio_venta
        )

        # 5. Guardar detalle
        return self.repo.save(detalle)
