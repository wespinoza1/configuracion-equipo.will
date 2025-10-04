from typing import List, Optional
from infrastructure.models.detalleventa_model import DetalleVentaModel
from infrastructure.models.notaventa_model import NotaVentaModel
from infrastructure.models.producto_model import ProductoModel
from core.entities.detalleventa import DetalleVenta


class DetalleVentaDjangoRepository:
    """Repositorio Django para la entidad DetalleVenta."""

    # ------------------ Métodos principales ------------------

    def save(self, entity: DetalleVenta) -> DetalleVenta:
        """Guarda o actualiza un detalle de venta en la BD."""
        model = self._map_entity_to_model(entity)
        model.save()
        return self._map_model_to_entity(model)

    def get_by_id(self, id: int) -> Optional[DetalleVenta]:
        """Obtiene un detalle de venta por ID."""
        try:
            model = DetalleVentaModel.objects.get(id=id)
            return self._map_model_to_entity(model)
        except DetalleVentaModel.DoesNotExist:
            return None

    def list_by_venta(self, notaventa_id: int) -> List[DetalleVenta]:
        """Lista los detalles de una nota de venta específica."""
        models = DetalleVentaModel.objects.filter(nota_id=notaventa_id)
        return [self._map_model_to_entity(m) for m in models]

    def list_all(self) -> List[DetalleVenta]:
        """Lista todos los detalles de todas las ventas."""
        models = DetalleVentaModel.objects.all()
        return [self._map_model_to_entity(m) for m in models]

    def delete(self, id: int) -> None:
        """Elimina un detalle de venta (delete físico)."""
        try:
            model = DetalleVentaModel.objects.get(id=id)
            model.delete()
        except DetalleVentaModel.DoesNotExist:
            raise ValueError("Detalle de venta no encontrado")

    # ------------------ 🔑 Mappers ------------------

    def _map_entity_to_model(self, entity: DetalleVenta) -> DetalleVentaModel:
        """Convierte una entidad DetalleVenta en modelo Django."""
        nota_model = NotaVentaModel.objects.get(id=entity.notaventa_id)
        producto_model = ProductoModel.objects.get(id=entity.producto_id)

        return DetalleVentaModel(
            id=entity.id,
            nota=nota_model,
            producto=producto_model,
            cantidad=entity.cantidad,
            precio_venta=entity.precio_venta
        )

    def _map_model_to_entity(self, model: DetalleVentaModel) -> DetalleVenta:
        """Convierte un modelo Django en entidad DetalleVenta."""
        return DetalleVenta(
            id=model.id,
            notaventa_id=model.nota.id,
            producto_id=model.producto.id,
            cantidad=model.cantidad,
            precio_venta=model.precio_venta
        )
# ------------------ Fin del archivo ------------------