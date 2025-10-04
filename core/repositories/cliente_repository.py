from abc import ABC, abstractmethod
from typing import List, Optional
from core.entities.cliente import Cliente

"""Contrato del repositorio de Cliente (independiente de infraestructura)."""
class ClienteRepository(ABC):

    @abstractmethod
    def save(self, cliente: Cliente) -> Cliente:
        """Guarda un cliente en el sistema (crear o actualizar)."""
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Cliente]:
        """Obtiene un cliente por su identificador único (int autoincremental)."""
        pass

    @abstractmethod
    def list_all(self) -> List[Cliente]:
        """Lista todos los clientes."""
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        """Elimina un cliente por su identificador (int autoincremental)."""
        pass
