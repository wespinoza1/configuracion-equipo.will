

''' codigo anterior
from core.entities.producto import Producto
from core.repositories.producto_repository import ProductoRepository
from typing import Optional



class RegistrarProducto:
    """Caso de uso para registrar un nuevo producto."""

    def __init__(self, repo: ProductoRepository):
        self.repo = repo


    """
    Crea y guarda un producto.

    Args:
        descripcion (str): Nombre o descripción del producto.
        precio (float): Precio del producto.
        stock (int): Cantidad disponible.
        categoria (Categoria): Instancia de la categoría asociada.

    Returns:
        Producto: Producto persistido.
        """
    def ejecutar(
        self,
        descripcion: str,
        precio: float,
        stock: int,
        categoria
    ) -> Producto:

        # Crear la entidad (validación automática en __post_init__)
        producto = Producto(
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            categoria=categoria
        )

        # Guardar usando el repositorio
        return self.repo.save(producto)
'''

from core.entities.producto import Producto
from core.repositories.producto_repository import ProductoRepository
from core.entities.categoria import Categoria


class RegistrarProducto:
    """Caso de uso para registrar un nuevo producto."""

    def __init__(self, repo: ProductoRepository):
        self.repo = repo

    def ejecutar(
        self,
        descripcion: str,
        precio: float,
        stock: int,
        categoria: Categoria
    ) -> Producto:
        """
        Crea y guarda un producto.

        Args:
            descripcion (str): Nombre o descripción del producto.
            precio (float): Precio del producto.
            stock (int): Cantidad disponible.
            categoria (Categoria): Instancia de la categoría asociada.

        Returns:
            Producto: Producto persistido.
        """

        # Extraer id de categoría (clave primaria)
        categoria_id = categoria.id
        if not categoria_id:
            raise ValueError("La categoría debe tener un ID válido para registrar un producto")

        # Crear la entidad (validación automática en __post_init__)
        producto = Producto(
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            categoria=categoria  # mantenemos la referencia completa
        )

        # Persistir usando solo el ID de la categoría en el repositorio
        return self.repo.save(producto)
