from typing import List, Optional
from core.entities.categoria import Categoria
from core.repositories.categoria_repository import CategoriaRepository
from infrastructure.models.categoria_model import CategoriaModel


class CategoriaDjangoRepository(CategoriaRepository):
    """Implementación de CategoriaRepository usando Django ORM."""

    def _map_to_entity(self, model: CategoriaModel) -> Categoria:
        """Convierte un modelo Django a entidad del dominio."""
        return Categoria(
            id=model.id,
            nombre=model.nombre,
            fecha_creacion=model.fecha_creacion,
            activa=model.activa,
        )

    def _map_to_model(self, entity: Categoria) -> CategoriaModel:
        """Convierte una entidad del dominio a modelo Django."""
        if entity.id:
            return CategoriaModel(
                id=entity.id,
                nombre=entity.nombre,
                fecha_creacion=entity.fecha_creacion,
                activa=entity.activa,
            )
        return CategoriaModel(
            nombre=entity.nombre,
            fecha_creacion=entity.fecha_creacion,
            activa=entity.activa,
        )

    def save(self, categoria: Categoria) -> Categoria:
        model = None
        if categoria.id:
            # Actualizar
            model = CategoriaModel.objects.get(pk=categoria.id)
            model.nombre = categoria.nombre
            model.activa = categoria.activa
            # La fecha_creacion no se actualiza
        else:
            # Crear nuevo
            model = CategoriaModel(
                nombre=categoria.nombre,
                activa=categoria.activa,
            )
        model.save()
        return self._map_to_entity(model)

    def get_by_id(self, id: int) -> Optional[Categoria]:
        try:
            model = CategoriaModel.objects.get(pk=id)
            return self._map_to_entity(model)
        except CategoriaModel.DoesNotExist:
            return None

    def get_by_nombre(self, nombre: str) -> Optional[Categoria]:
        try:
            model = CategoriaModel.objects.get(nombre__iexact=nombre.strip())
            return self._map_to_entity(model)
        except CategoriaModel.DoesNotExist:
            return None

    def list_all(self) -> List[Categoria]:
        #models = CategoriaModel.objects.all().order_by("nombre")----no se ve bien que ordene el json asi
        models = CategoriaModel.objects.all()
        return [self._map_to_entity(m) for m in models]

    
    #version delete anterior, para usar una mejorada
    #def delete(self, id: int) -> None:
    #    CategoriaModel.objects.filter(pk=id).delete()

    def delete(self, id: int) -> None:
        """Soft delete en lugar de eliminación física"""
        try:
            obj = CategoriaModel.objects.get(id=id)
            obj.soft_delete()  # 👈 usamos el método del modelo
        except CategoriaModel.DoesNotExist:
            pass