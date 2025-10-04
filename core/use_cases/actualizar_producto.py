from core.entities.producto import Producto
from core.repositories.producto_repository import ProductoRepository
from core.repositories.categoria_repository import CategoriaRepository


class ActualizarProducto:
    """Caso de uso para actualizar un producto existente."""

    def __init__(self, producto_repo: ProductoRepository, categoria_repo: CategoriaRepository):
        self.producto_repo = producto_repo
        self.categoria_repo = categoria_repo

    def ejecutar(
        self,
        producto_id: int,
        descripcion: str,
        precio: float,
        stock: int,
        categoria_id: int,
        activo: bool
    ) -> Producto:
        """
        Actualiza y guarda un producto validando la categoría.
        """

        # Validar producto existente
        producto_actual = self.producto_repo.get_by_id(producto_id)
        if not producto_actual:
            raise ValueError("Producto no encontrado")

        # Validar categoría
        categoria = self.categoria_repo.get_by_id(categoria_id)
        if not categoria or not categoria.activa:
            raise ValueError("Categoría inválida o inactiva")

        # Crear nueva entidad (inmutable)
        producto_actualizado = Producto(
            id=producto_actual.id,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            categoria=categoria,  # asignamos la entidad completa
            activo=activo
        )

        # Persistir
        return self.producto_repo.save(producto_actualizado)

