from typing import Optional, ClassVar
from dataclasses import dataclass
from core.entities.categoria import Categoria


@dataclass(frozen=True)

class Producto:
    """Entidad que representa un producto en el sistema."""

    descripcion: str
    precio: float
    stock: int
    categoria: Categoria
    id: Optional[int] = None
    activo: bool = True

    # Constantes de validación
    DESCRIPCION_MIN_LENGTH: ClassVar[int] = 3
    DESCRIPCION_MAX_LENGTH: ClassVar[int] = 100
    PRECIO_MIN: ClassVar[float] = 0.01
    STOCK_MIN: ClassVar[int] = 0

    def __post_init__(self):
        self._validar()

    def _validar(self):
        """Validaciones de negocio del producto."""

        # Normalizar descripción
        object.__setattr__(self, 'descripcion', self.descripcion.strip().title())

        # Validar longitud de descripción
        if len(self.descripcion) < self.DESCRIPCION_MIN_LENGTH:
            raise ValueError(f"La descripción debe tener al menos {self.DESCRIPCION_MIN_LENGTH} caracteres")
        if len(self.descripcion) > self.DESCRIPCION_MAX_LENGTH:
            raise ValueError(f"La descripción no puede exceder {self.DESCRIPCION_MAX_LENGTH} caracteres")

        # Validar precio
        if self.precio < self.PRECIO_MIN:
            raise ValueError(f"El precio debe ser al menos {self.PRECIO_MIN}")

        # Validar stock
        if self.stock < self.STOCK_MIN:
            raise ValueError(f"El stock no puede ser menor a {self.STOCK_MIN}")

        # Validar categoría
        if not isinstance(self.categoria, Categoria):
            raise ValueError("La categoría debe ser una instancia de Categoria")

    @property
    def es_nuevo(self) -> bool:
        """Indica si el producto aún no ha sido persistido."""
        return self.id is None

    def activar(self) -> 'Producto':
        """Activa el producto (inmutable)."""
        return Producto(
            id=self.id,
            descripcion=self.descripcion,
            precio=self.precio,
            stock=self.stock,
            categoria=self.categoria,
            activo=True
        )

    def desactivar(self) -> 'Producto':
        """Desactiva el producto (inmutable)."""
        return Producto(
            id=self.id,
            descripcion=self.descripcion,
            precio=self.precio,
            stock=self.stock,
            categoria=self.categoria,
            activo=False
        )

    def __eq__(self, other):
        if not isinstance(other, Producto):
            return False
        if self.id and other.id:
            return self.id == other.id
        return self.descripcion.lower() == other.descripcion.lower()

    def __hash__(self):
        return hash(self.id) if self.id else hash(self.descripcion.lower())

    def tiene_stock(self, cantidad: int) -> bool:
        """Verifica si hay suficiente stock para vender."""
        return self.stock >= cantidad

    def disminuir_stock(self, cantidad: int) -> 'Producto':
        """Devuelve una nueva instancia con stock reducido."""
        if not self.tiene_stock(cantidad):
            raise ValueError("No hay suficiente stock disponible")
        return Producto(
            id=self.id,
            descripcion=self.descripcion,
            precio=self.precio,
            stock=self.stock - cantidad,
            categoria=self.categoria,
            activo=self.activo
        )
