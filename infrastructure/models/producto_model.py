from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from infrastructure.models.categoria_model import CategoriaModel

class ProductoModel(models.Model):
    """Modelo Django para productos."""

    descripcion = models.CharField(max_length=100,unique=True)

    precio = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    stock = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )

    categoria = models.ForeignKey(
        CategoriaModel,
        on_delete=models.PROTECT,  # evita eliminar categoría si hay productos asociados
        related_name='productos'
    )
    
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']

    def __str__(self):
        return self.descripcion
    
    def clean(self):
        super().clean()
        if self.stock < 0:
            raise ValidationError("El stock no puede ser negativo.")


    # ----------------------------
    # Métodos de activación / soft delete
    # ----------------------------
    def soft_delete(self):
        """Desactiva el producto (soft delete)."""
        self.activo = False
        self.save(update_fields=['activo'])

    def activate(self):
        """Activa el producto."""
        self.activo = True
        self.save(update_fields=['activo'])

    
