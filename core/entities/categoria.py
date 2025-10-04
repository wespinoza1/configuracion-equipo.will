from typing import Optional, ClassVar
import re
from dataclasses import dataclass, field
from datetime import datetime

@dataclass(frozen=True, eq=False)
class Categoria:
    """Entidad que representa una categoría de productos."""    
    id: Optional[int] = None
    nombre: str = field(default="")
    fecha_creacion: datetime = field(default_factory=datetime.now)
    activa: bool = True

    NOMBRE_MIN_LENGTH: ClassVar[int] = 3
    NOMBRE_MAX_LENGTH: ClassVar[int] = 50
    NOMBRE_PATTERN: ClassVar[str] = r'^[a-zA-ZáéíóúñÑ\s]+$'
    
    def __post_init__(self):
        self._normalizar_y_validar()
    
    def _normalizar_y_validar(self):
        # Normalizar
        object.__setattr__(self, 'nombre', self.nombre.strip().title())
        
        # Validaciones
        if len(self.nombre) < self.NOMBRE_MIN_LENGTH:
            raise ValueError(f"El nombre debe tener al menos {self.NOMBRE_MIN_LENGTH} caracteres")
        
        if len(self.nombre) > self.NOMBRE_MAX_LENGTH:
            raise ValueError(f"El nombre no puede exceder {self.NOMBRE_MAX_LENGTH} caracteres")
        
        if not re.match(self.NOMBRE_PATTERN, self.nombre):
            raise ValueError("El nombre solo puede contener letras y espacios")
    
    @property
    def es_nueva(self) -> bool:
        """Indica si es una categoría no persistida"""
        return self.id is None
    
    def activar(self) -> 'Categoria':
        """Marca la categoría como activa"""
        return Categoria(
            id=self.id, nombre=self.nombre,
            fecha_creacion=self.fecha_creacion, activa=True
        )
    
    def desactivar(self) -> 'Categoria':
        return Categoria(
            id=self.id, nombre=self.nombre,
            fecha_creacion=self.fecha_creacion, activa=False
        )
    
    def __eq__(self, other):
        if not isinstance(other, Categoria):
            return False
        if self.id and other.id:
            return self.id == other.id
        return self.nombre.lower() == other.nombre.lower()
    
    def __hash__(self):
        return hash(self.id) if self.id else hash(self.nombre.lower())
    
    def __str__(self):
        return f"Categoria({self.nombre}, {'Activa' if self.activa else 'Inactiva'})"
