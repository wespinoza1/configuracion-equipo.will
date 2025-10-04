from abc import ABC, abstractmethod
from typing import List, Optional
from core.entities.categoria import Categoria

class CategoriaRepository(ABC):
    """Contrato del repositorio de Categoría (independiente de infraestructura)."""

    @abstractmethod
    def save(self, categoria: Categoria) -> Categoria:
        """Guarda o actualiza una categoría en el sistema."""
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Categoria]:
        """Obtiene una categoría por su identificador único."""
        pass

    @abstractmethod
    def get_by_nombre(self, nombre: str) -> Optional[Categoria]:
        """Obtiene una categoría por su nombre (si existe)."""
        pass
    
    @abstractmethod
    def list_all(self) -> List[Categoria]:
        """Lista todas las categorías registradas."""
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        """Elimina una categoría por su identificador."""
        pass

