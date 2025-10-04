from django.db import models
from django.utils import timezone
from infrastructure.models.cliente_model import ClienteModel

class NotaVentaModel(models.Model):
    cliente = models.ForeignKey(
        ClienteModel,
        on_delete=models.CASCADE,  # Si el cliente se elimina, eliminamos sus notas
        related_name='notas_venta'
    )
    monto = models.FloatField()
    fecha = models.DateTimeField(default=timezone.now)  # Permite pasar fecha manual o usar la actual
    activo = models.BooleanField(default=True)          # Soft delete

    class Meta:
        db_table = 'notas_venta'
        verbose_name = 'Nota de Venta'
        verbose_name_plural = 'Notas de Venta'
        ordering = ['id']

    def __str__(self):
        return f"Nota #{self.id} - Cliente: {self.cliente.nombre} - Monto: {self.monto}"

    def soft_delete(self):
        """Eliminación lógica de la nota de venta"""
        self.activo = False
        self.save(update_fields=['activo'])

    def activate(self):
        """Reactivar nota de venta"""
        self.activo = True
        self.save(update_fields=['activo'])
