from django.db import models
from infrastructure.models.notaventa_model import NotaVentaModel
from infrastructure.models.producto_model import ProductoModel


class DetalleVentaModel(models.Model):
    """
    Modelo Django que representa un detalle de venta.
    Tabla intermedia entre NotaVenta y Producto con atributos adicionales.
    """

    nota = models.ForeignKey(
        NotaVentaModel,
        on_delete=models.CASCADE,
        related_name="detalles"
    )
    producto = models.ForeignKey(
        ProductoModel,
        on_delete=models.CASCADE,
        related_name="detalles"
    )
    cantidad = models.PositiveIntegerField(default=1)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "detalle_venta"
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Venta"
        unique_together = ("nota", "producto")  # Evita duplicados en una misma nota

    def __str__(self):
        return f"DetalleVenta(nota={self.nota_id}, producto={self.producto_id}, cantidad={self.cantidad})"
