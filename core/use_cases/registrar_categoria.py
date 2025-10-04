from typing import Optional
from core.entities.categoria import Categoria
from core.repositories.categoria_repository import CategoriaRepository


class RegistrarCategoria:

    """Caso de uso: Registrar una nueva categoría en el sistema."""

    def __init__(self, categoria_repository: CategoriaRepository):
        self.categoria_repository = categoria_repository

    #execute-->ejecutar
    def ejecutar(self, nombre: str, activa: Optional[bool] = True) -> Categoria:
        
        # 1. Validar si ya existe una categoría con ese nombre
        existente = self.categoria_repository.get_by_nombre(nombre)
        if existente is not None:
            raise ValueError(f"Ya existe una categoría con el nombre '{nombre}'")

        # 2. Crear la entidad (la validación del nombre la hace la propia entidad)
        categoria = Categoria(nombre=nombre, activa=activa)

        # 3. Guardar en el repositorio
        return self.categoria_repository.save(categoria)
