from abc import ABC, abstractmethod
from typing import List, Optional
from core.entities.detalleventa import DetalleVenta

class DetalleVentaRepository(ABC):
    """Contrato del repositorio para la entidad DetalleVenta"""

    @abstractmethod
    def save(self, detalle: DetalleVenta) -> DetalleVenta:
        """Guarda o actualiza un detalle de venta"""
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[DetalleVenta]:
        """Obtiene un detalle de venta por su ID"""
        pass

    @abstractmethod
    def list_by_venta(self, notaventa_id: int) -> List[DetalleVenta]:
        """Lista todos los detalles asociados a una nota de venta"""
        pass

    @abstractmethod
    def list_all(self) -> List[DetalleVenta]:
        """Lista todos los detalles de venta"""
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        """Elimina un detalle de venta (soft delete o físico)"""
        pass
