from abc import ABC, abstractmethod
from typing import List, Optional, Union
from core.entities.notaventa import NotaVenta

class NotaVentaRepository(ABC):
    """Contrato de repositorio para persistir y consultar Notas de Venta."""

    @abstractmethod
    def save(self, nota: NotaVenta) -> NotaVenta:
        """Guarda o actualiza una nota de venta en el sistema."""
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[NotaVenta]:
        """Obtiene una nota de venta por su identificador único."""
        pass

    @abstractmethod
    def list_all(self) -> List[NotaVenta]:
        """Lista todas las notas de venta."""
        pass

    @abstractmethod
    def list_by_cliente(self, cliente_id: int) -> List[NotaVenta]:
        """Lista todas las notas de venta de un cliente específico."""
        pass

    @abstractmethod
    def delete(self, id: Union[int, str], soft: bool = True) -> None:
        """
        Elimina una nota de venta por su identificador.
        
        :param id: Identificador único de la nota de venta
        :param soft: Si es True, realiza un soft delete (ej. marca como inactiva).
                     Si es False, elimina definitivamente el registro.
        """
        pass