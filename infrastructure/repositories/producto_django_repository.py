from typing import List, Optional
from core.entities.producto import Producto
from core.entities.categoria import Categoria
from core.repositories.producto_repository import ProductoRepository
from infrastructure.models.producto_model import ProductoModel


class ProductoDjangoRepository(ProductoRepository):
    """Implementación de ProductoRepository usando Django ORM."""

    def save(self, producto: Producto) -> Producto:
        obj, created = ProductoModel.objects.update_or_create(
            id=producto.id,
            defaults={
                "descripcion": producto.descripcion,
                "precio": producto.precio,
                "stock": producto.stock,
                "categoria_id": producto.categoria.id,  # ✅ se extrae desde la entidad
                "activo": producto.activo,
            }
        )
        return self._map_to_entity(obj)

    def get_by_id(self, id: int) -> Optional[Producto]:
        try:
            obj = ProductoModel.objects.get(id=id, activo=True)
            return self._map_to_entity(obj)
        except ProductoModel.DoesNotExist:
            return None

    def get_by_descripcion(self, descripcion: str) -> Optional[Producto]:
        try:
            obj = ProductoModel.objects.get(
                descripcion__iexact=descripcion.strip(),
                activo=True
            )
            return self._map_to_entity(obj)
        except ProductoModel.DoesNotExist:
            return None

    def list_all(self) -> List[Producto]:
        return [self._map_to_entity(obj) for obj in ProductoModel.objects.filter(activo=True)]

    def delete(self, id: int) -> None:
        """Soft delete del producto."""
        try:
            obj = ProductoModel.objects.get(id=id)
            obj.soft_delete()
        except ProductoModel.DoesNotExist:
            pass

    def list_by_categoria(self, categoria_id: int) -> List[Producto]:
        return [
            self._map_to_entity(obj)
            for obj in ProductoModel.objects.filter(categoria_id=categoria_id, activo=True)
        ]

    def _map_to_entity(self, obj: ProductoModel) -> Producto:
        categoria = Categoria(
            id=obj.categoria.id,
            nombre=obj.categoria.nombre,
            activa=obj.categoria.activa
        )
        return Producto(
            id=obj.id,
            descripcion=obj.descripcion,
            precio=float(obj.precio),
            stock=obj.stock,
            categoria=categoria,   # ✅ siempre se devuelve la entidad Categoria
            activo=obj.activo
        )
