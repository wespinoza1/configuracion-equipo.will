from abc import ABC, abstractmethod
from typing import List, Optional
from core.entities.producto import Producto


class ProductoRepository(ABC):
    """Contrato del repositorio de Producto (independiente de la infraestructura)."""

    @abstractmethod
    def save(self, producto: Producto) -> Producto:
        """Guarda un producto en el sistema (crear o actualizar)."""
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Producto]:
        """Obtiene un producto activo por su ID único."""
        pass

    @abstractmethod
    def get_by_descripcion(self, descripcion: str) -> Optional[Producto]:
        """Obtiene un producto activo por su descripción."""
        pass

    @abstractmethod
    def list_all(self) -> List[Producto]:
        """Lista todos los productos activos."""
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        """Desactiva un producto por su ID (soft delete)."""
        pass

    @abstractmethod
    def list_by_categoria(self, categoria_id: int) -> List[Producto]:
        """Lista todos los productos activos de una categoría específica."""
        pass
