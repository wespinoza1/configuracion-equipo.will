from typing import Optional
from infrastructure.models.notaventa_model import NotaVentaModel
from infrastructure.models.cliente_model import ClienteModel
from core.entities.notaventa import NotaVenta


class NotaVentaDjangoRepository:
    """Repositorio Django para persistir Notas de Venta."""

    def save(self, entity: NotaVenta) -> NotaVenta:
        model = self._map_entity_to_model(entity)
        model.save()
        return self._map_model_to_entity(model)

    def get_by_id(self, id: int) -> Optional[NotaVenta]:
        try:
            model = NotaVentaModel.objects.get(id=id, activo=True)  # ✅ solo notas activas
            return self._map_model_to_entity(model)
        except NotaVentaModel.DoesNotExist:
            return None

    def list_all(self) -> list[NotaVenta]:
        models = NotaVentaModel.objects.filter(activo=True)
        return [self._map_model_to_entity(m) for m in models]

    def list_by_cliente(self, cliente_id: int) -> list[NotaVenta]:
        models = NotaVentaModel.objects.filter(cliente_id=cliente_id, activo=True)
        return [self._map_model_to_entity(m) for m in models]

    def delete(self, id: int) -> None:
        try:
            model = NotaVentaModel.objects.get(id=id)
            model.soft_delete()  # ✅ cambia activo=False y guarda
        except NotaVentaModel.DoesNotExist:
            raise ValueError("Nota de venta no encontrada")

    # ------------------ 🔑 Mapeadores ------------------

    def _map_entity_to_model(self, entity: NotaVenta) -> NotaVentaModel:
        """Convierte una entidad NotaVenta a modelo Django."""
        cliente_model = ClienteModel.objects.get(id=entity.cliente_id)
        return NotaVentaModel(
            id=entity.id,
            cliente=cliente_model,
            monto=entity.monto,
            fecha=entity.fecha,
            activo=entity.activo  # ✅ usa el valor real de la entidad
        )

    def _map_model_to_entity(self, model: NotaVentaModel) -> NotaVenta:
        """Convierte un modelo Django a entidad NotaVenta."""
        return NotaVenta(
            id=model.id,
            cliente_id=model.cliente.id,
            monto=model.monto,
            fecha=model.fecha,
            activo=model.activo  # ✅ mapeamos también el activo
        )
